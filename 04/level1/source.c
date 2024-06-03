#include <stdio.h>
#include <string.h>

int main()
{
	char password[1024];

	printf("Please enter key: ");
	scanf("%s", password);

	if (!strcmp(password, "__stack_check"))
	{
		printf("Good job.\n");
	}
	else
	{
		printf("Nope.\n");
	}
	return (0);
}
