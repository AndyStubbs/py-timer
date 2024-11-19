# Py-Timer

**Py-Timer** is a command-line application written in Python that allows you to create, manage, and monitor timers for various activities. It is a lightweight and efficient tool designed for users who prefer using the terminal for task management and time tracking.

---

## Features

- **Multiple Timers**: Manage multiple timers simultaneously for different tasks or activities.
- **Command-Line Control**: Use simple command-line arguments to interact with the timers.
- **Real-Time Updates**: View timers ticking in real-time.
- **Flexible Timer Management**: Start, pause, reset, and resume timers easily.

---

## Setup Instructions

### Prerequisites

This app was written and tested using Python version 3.12.6. You can download it from the [official Python website](https://www.python.org/downloads/).

### Cloning the Repository

To clone the repository, use the following command:

```sh
git clone https://github.com/AndyStubbs/py-timer.git
```

Navigate to the project directory:

```sh
cd py-timer
```

### Running the Program

To run the program, execute the following command:

```sh
python main.py -h
```

This will start the Py-Timer application and give you a list of all the command line options.

---

## Usage

The `main.py` command is used with specific options to perform various tasks. Below is a detailed explanation of the usage:

```plaintext
Usage: main.py ["Timer Name"] [options]

Options:
  -h, --help        Show help information.
  -l, --list        Show a list of active timers.
  -p, --pause       Pause a specific timer.
  -r, --reset       Reset a specific timer to zero.
  -s, --start       Start or resume a timer. If the timer doesn't exist, a new one will be created.
  -t, --tick        Show all timers in real-time, updating continuously.
```

---

### Creating an Alias for Easier Usage

To simplify running the `pytimer` command, you can create an alias or script based on your operating system:

#### Windows
1. Create a `.bat` file to link to the `main.py` file:
   - Open a text editor and paste the following code, replacing `path\to\pytimer\main.py` with the full path to the `main.py` file:
     ```
     @echo off
     python "path\to\pytimer\main.py" %*
     ```
   - Save the file as `pytimer.bat`.

2. Add the location of the `.bat` file to your system's PATH:
   - Right-click on "This PC" or "My Computer" and select **Properties**.
   - Go to **Advanced System Settings** > **Environment Variables**.
   - In the "System variables" section, find the "Path" variable and click **Edit**.
   - Add the directory containing the `pytimer.bat` file.

3. Open a new Command Prompt and run `pytimer`:

#### BASH (Linux/macOS)

To create an alias for easier usage of the `pytimer` command:

1. Open your shell configuration file in a text editor. The file is typically located at:
   - `~/.bashrc` (for Bash users)
   - `~/.zshrc` (for Zsh users)
   - `~/.bash_profile` (alternative for Bash on some systems)

2. Add the following line, replacing `/path/to/pytimer/main.py` with the full path to the `main.py` file:
   ```bash
   alias pytimer='python3 /path/to/pytimer/main.py'
3. Save the file and reload your shell configuration by running:
   ```bash
   source ~/.bashrc  # For Bash users
   # or
   source ~/.zshrc   # For Zsh users
   ```

---

## Examples

### Show Help Information
To display the help information, use the following command:
```sh
pytimer -h
```

### List Active Timers
To list all active timers, use the following command:
```sh
pytimer -l
```

### Pause a Timer
To pause a specific timer, use the following command:
```sh
pytimer "Work Timer" -p
```

### Reset a Timer
To reset a specific timer to zero, use the following command:
```sh
pytimer "Work Timer" -r
```

### Start or Resume a Timer
To start or resume a timer, use the following command:
```sh
pytimer "Work Timer" -s
```

### Show Timers in Real-Time
To show all timers in real-time, updating continuously, use the following command:
```sh
pytimer -t
```
