from typing import List, Iterator
from pyspark.sql import SparkSession
import glob
import logging
import os
import shutil


class FileIOBase:
    """
    Base class for file io
    """
    def list(self, dir_path) -> Iterator[str]:
        """
        List files in a directory
        """
        raise NotImplementedError("list is not implemented")

    def rename(self, src_path: str, dst_path: str) -> bool:
        """
        Rename a file or directory
        """
        raise NotImplementedError("rename is not implemented")

    def remove(self, file_path: str) -> bool:
        """
        Remove a file
        """
        raise NotImplementedError("remove is not implemented")

    def remove_directory(self, dir_path: str) -> bool:
        """
        Remove a directory
        """
        raise NotImplementedError("remove_directory is not implemented")

    def get_create_time(self, file_path: str) -> int:
        """
        Create time of a file or directory (milliseconds since 1970-01-01 00:00:00)
        """
        raise NotImplementedError("create_time is not implemented")

    def get_file_size(self, file_path: str) -> int:
        """
        Size of a file
        """
        raise NotImplementedError("get_file_size is not implemented")

    def glob(self, file_path: str) -> Iterator[str]:
        """
        Glob files
        """
        raise NotImplementedError("glob is not implemented")

    def list_valid_files(self, dir_path: str) -> Iterator[str]:
        """
        List valid files in a directory
        """
        raise NotImplementedError("list_valid_files is not implemented")

    def read(self, file_path: str) -> bytes:
        raise NotImplementedError("read is not implemented")


class Posix(FileIOBase):
    def list(self, dir_path) -> Iterator[str]:
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                yield os.path.join(root, file)

    def rename(self, src_path: str, dst_path: str) -> bool:
        try:
            os.rename(src_path, dst_path)
            return True
        except Exception as ex:
            logging.exception(ex)
            return False

    def remove(self, file_path: str) -> bool:
        try:
            os.remove(file_path)
            return True
        except Exception as ex:
            logging.exception(ex)
            return False

    def remove_directory(self, dir_path: str) -> bool:
        try:
            shutil.rmtree(dir_path)
            return True
        except Exception as ex:
            logging.exception(ex)
            return False
    
    def get_create_time(self, file_path: str) -> int:
        return int(os.path.getctime(file_path) * 1000)

    def get_file_size(self, file_path: str) -> int:
        return os.path.getsize(file_path)

    def is_exists(self, file_path: str) -> bool:
        return os.path.exists(file_path)

    def is_directory(self, file_path: str) -> bool:
        return os.path.isdir(file_path)

    def glob(self, file_path: str) -> Iterator[str]:
        for file in glob.glob(file_path):
            yield file

    def list_valid_files(self, dir_path: str) -> Iterator[str]:
        for root, _, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.isfile(file_path) and file != '_SUCCESS' and not file.startswith('.') and os.path.getsize(
                        file_path) > 0:
                    yield file_path
                else:
                    logging.info(f'过滤掉无效文件: {file_path}')

    def read(self, file_path: str) -> bytes:
        with open(file_path, 'rb') as f:
            return f.read()


class HDFS(FileIOBase):
    def __init__(self, spark: SparkSession):
        self.spark = spark
        self.sc = spark.sparkContext
        self.hadoop_conf = spark._jsc.hadoopConfiguration()
        self.URI = self.sc._gateway.jvm.java.net.URI
        self.Path = self.sc._gateway.jvm.org.apache.hadoop.fs.Path
        self.FileSystem = self.sc._gateway.jvm.org.apache.hadoop.fs.FileSystem
        self.Configuration = self.sc._gateway.jvm.org.apache.hadoop.conf.Configuration
        self.fs = self.FileSystem.get(self.hadoop_conf)

    def list(self, dir_path: str) -> Iterator[str]:
        for item in self.fs.listStatus(self.Path(dir_path)):
            yield item.getPath().toString()

    def rename(self, src_path: str, dst_path: str) -> bool:
        return self.fs.rename(self.Path(src_path), self.Path(dst_path))

    def remove(self, file_path: str) -> bool:
        return self.fs.delete(self.Path(file_path), False)

    def remove_directory(self, dir_path: str) -> bool:
        return self.fs.delete(self.Path(dir_path), True)

    def get_create_time(self, file_path: str) -> int:
        return self.fs.getFileStatus(self.Path(file_path)).getModificationTime()

    def get_file_size(self, file_path: str) -> int:
        return self.fs.getFileStatus(self.Path(file_path)).getLen()

    def is_exists(self, file_path: str) -> bool:
        return self.fs.exists(self.Path(file_path))
    
    def is_directory(self, file_path: str) -> bool:
        return self.fs.getFileStatus(self.Path(file_path)).isDirectory()

    def glob(self, file_path: str) -> Iterator[str]:
        file_status = self.fs.globStatus(self.Path(file_path))
        for file in file_status:
            yield file.getPath().toString()

    def list_valid_files(self, dir_path: str) -> Iterator[str]:
        for item in self.fs.listStatus(self.Path(dir_path)):
            name = item.getPath().getName()
            if not item.isDirectory() and name != '_SUCCESS' and not name.startswith('.') and item.getLen() > 0:
                yield item.getPath().toString()
            else:
                logging.info(f'过滤掉无效文件: {item.getPath().toString()}')

    def read(self, file_path: str) -> bytes:
        f = None
        try:
            f = self.fs.open(self.Path(file_path))
            # 建立临时缓冲区
            BUFFER_SIZE = 4096 # 4KB
            byte_buffer = self.spark._jvm.java.nio.ByteBuffer.allocate(BUFFER_SIZE)
            # 存储所有读取的数据
            all_bytes = bytearray()
            while True:
                # 读取数据到 ByteBuffer
                bytes_read = f.read(byte_buffer)
                if bytes_read > 0:
                    # 切换到读取模式
                    byte_buffer.flip()
                    # 将 ByteBuffer 转换为字节数组并追加到 all_bytes
                    all_bytes.extend(byte_buffer.array()[:bytes_read])
                    # 清除 ByteBuffer 以准备下一次读取
                    byte_buffer.clear()
                else:
                    break  # 文件末尾跳出循环
            return bytes(all_bytes)
        finally:
            if f:
                f.close()
