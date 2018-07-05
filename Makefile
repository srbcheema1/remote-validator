all:
	echo "all"

compile:
	echo "compiling proto file"
	python -m grpc_tools.protoc -I./include --python_out=. --grpc_python_out=. include/validator.proto

clean:
	rm *pb2*
