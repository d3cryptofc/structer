# Contributing

Here is a guide showing how to contribute to the project the right way, everyone is welcome, and thank you for being interested in this project!

#### 1. Install [UV](https://docs.astral.sh/uv/getting-started/installation/) project manager:

Tool responsible for managing project dependencies, virtual environment and more.

- From bash script:

  ```
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

- From pacman (Arch Linux):

  ```
  sudo pacman -Sy && sudo pacman -S uv
  ```

- From PyPI:

  ```
  pip3 install uv
  ```

#### 2. Setup hooks:

Implement custom hooks to avoid sending commits that have not been tested, formatted, or verified by linters.

```
task githooks
```

#### 3. Create your own branch:

- For a new feature:

  ```
  git checkout -b feature/your-feature-short-name
  ```

- For a new fix:

  ```
  git checkout -b fix/your-bug-short-name
  ```


#### 4. Install project packages and activate virtual environment:

Creates a virtual environment, installs the external packages that the project uses, and activates the virtual environment (`uv sync` is only needed once).

```
uv sync && source .venv/bin/activate
```

#### 5. Make a pull request to the `develop` branch if it's possible.

The `main` branch is dedicated to final versions, we use the `develop` branch for development and merge it to `main` when it is ready for a release.