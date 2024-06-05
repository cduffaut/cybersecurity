all:
	docker build -t stockholm .
	docker run -it stockholm

clean:
	docker rmi stockholm

.PHONY: all clean fclean
