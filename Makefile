all:
	echo "all"

compile:
	echo "compiling proto file"
	# -I is equivalent to -proto_path
	python -m grpc_tools.protoc -I=proto/ --python_out=proto/ --grpc_python_out=proto/ proto/validator.proto

clean:
	rm *pb2*

cpp:
	g++ ./spike/cpp/demo.cpp -o bin/demo
	g++ ./spike/cpp/even.cpp -o bin/even
