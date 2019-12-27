# Habits

![Licencia MIT](https://img.shields.io/badge/Licencia-MIT-green)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/b3e704c3f150404582cd23b9fcb4be32)](https://www.codacy.com/manual/atareao/habits?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=atareao/habits&amp;utm_campaign=Badge_Grade)
[![CodeFactor](https://www.codefactor.io/repository/github/atareao/habits/badge/master)](https://www.codefactor.io/repository/github/atareao/habits/overview/master)

[![Twitter: atareao](https://img.shields.io/twitter/follow/atareao.svg?style=social)](https://twitter.com/atareao)

Habits is an application to monitor your habits with your PC. So you can study how many kilometers travel with your
mouse or how many keystrokes.

[![Habits](./data/icons/habits.svg)](https://www.atareao.es/aplicacion/habits/)


## Prerequisites

Before you begin, ensure you have met the following requirements:

* If you install it from PPA don't worry about, becouse all the requirements are included in the package
* If you clone the repository, you need, at least, these dependecies,

```
gir1.2-gtk-3.0,
gir1.2-glib-2.0,
gir1.2-gdkpixbuf-2.0,
gir1.2-appindicator3-0.1,
gir1.2-webkit2-4.0,
python3-xlib
```

## Installing Habits

To install **Habits**, follow these steps:

* In a terminal (`Ctrl+Alt+T`), run these commands

```
sudo add-apt-repository ppa:atareao/atareao
sudo apt update
sudo apt install habits
```

## Using Habits

To use **Habits**, open Habits, and configure it. After init **Habits** you see a window like this one for USB,

![start Habits](./screenshots/image01.png)

If you select bluetooth then,

![bluetooth](./screenshots/image02.png)

To add a new device click on `add device` in the menu,

![add device](./screenshots/image03.png)

Then select the device you want to use to unlock Ubuntu, Linux Mint, etc.

![select device](./screenshots/image04.png)


## Contributing to Habits

To contribute to **Habits**, follow these steps:

1. Fork this repository.
2. Create a branch: `git checkout -b <branch_name>`.
3. Make your changes and commit them: `git commit -m '<commit_message>'`
4. Push to the original branch: `git push origin <project_name>/<location>`
5. Create the pull request.

Alternatively see the GitHub documentation on [creating a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

## Contributors

Thanks to the following people who have contributed to this project:

* [@atareao](https://github.com/atareao)

You might want to consider using something like the [All Contributors](https://github.com/all-contributors/all-contributors) specification and its [emoji key](https://allcontributors.org/docs/en/emoji-key).

## Contact

If you want to contact me you can reach me at [atareao.es](https://www.atareao.es).

## License

This project uses the following license: [MIT License](https://choosealicense.com/licenses/mit/).
