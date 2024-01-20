# App_dev_1_workshop

`pip freeze` is a command-line tool that displays a list of installed packages and their versions. You can use this command to create a requirements.txt file that captures the dependencies of your Python project. Here's how you can do it:

1. Open a terminal or command prompt.

2. Navigate to your project directory using the `cd` command.

3. Run the following command to generate a `requirements.txt` file:

    ```bash
    pip freeze > requirements.txt
    ```

   This command redirects the output of `pip freeze` to a file named `requirements.txt`. The file will contain a list of all installed packages and their versions.

4. You can view the contents of the `requirements.txt` file using a text editor or by using the `cat` command on Unix-based systems or `type` command on Windows:

    ```bash
    cat requirements.txt  # Unix-based systems
    type requirements.txt  # Windows
    ```

The `requirements.txt` file can be used to recreate the environment on another machine or share the project's dependencies with others. To install the dependencies listed in `requirements.txt`, you can use the following command:

```bash
pip install -r requirements.txt
```

This command reads the requirements from the file and installs the specified packages and versions.

Remember to update your `requirements.txt` file whenever you add or remove dependencies from your project by rerunning the `pip freeze` command.
