all:
	echo "all"

compile:
	echo "compiling proto file"
	python -m grpc_tools.protoc -I./include --python_out=./lib --grpc_python_out=./lib include/validator.proto

clean:
	rm -f -r lib
	mkdir lib
