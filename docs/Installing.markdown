# Installing PATKIT

## Requisites

- A computer with a relatively new operating system which has a fairly regular
  file system.
- While pads and phones and watches are computers, PATKIT sadly does not run on
  them. ChromeOS may work, but it is a borderline case as the filesystem is a bit
  exotic for our purposes.
- A Linux, a Mac, or a Windows machine should be fine as long as it is capable
  of running a recent version of Python.
- If issues crop up, get in touch, and we'll see what can be done.

Currently, PATKIT is tested to work on
- PopOS 24.04, which means any recent Ubuntu-like system should be fine.

You only need to care about the detailed dependencies if you do not use uv or
pip for installing. In that case, see the `pyproject.toml` file for a full list
or the `uv.lock` for an even fuller list. If you do decide to use some other
system for installation, please get in touch -- we'd love to have the recipe in
case others need/want it.

## Installing for regular use

Do get in touch if you would like to *test* any of these. A downloadable
executable will hopefully also become reality. Do get in touch if you would like
to *develop* it.

Meanwhile `uv` and `pip` are valid options.

### Using uv

Once the [PyPi](https://pypi.org/search/?q=patkit) package exists this
simplifies to:
- Install [uv](https://docs.astral.sh/uv/#getting-started).
- On the commandline run `uv tool install patkit`.
- Running [instructions](Running.markdown).

### Using pip

Patkit is on [PyPi](https://pypi.org/search/?q=patkit):

- First install python either using your OS's software shop features or from
  [the official download page](https://www.python.org/downloads/).
- Second, run `pip install patkit`.

## Installing for development

### Using uv

Some care and understanding is needed if you want to have a installed released
version of Patkit and at the same time run local development versions for
testing. This can be done however. Use the instructions above for the released
install, and the instructions below for running the local versions.

- Install [uv](https://docs.astral.sh/uv/#getting-started).
- Fork patkit on [github](https://github.com/giuthas/patkit) if you like, or
  just clone it directly with `git clone https://github.com/giuthas/patkit` or
  download [the latest
  sources](https://github.com/giuthas/patkit/releases/latest).
- Optionally run these to get Patkit installed as a commandline tool. Skip
  this part if you have a released version of Patkit installed.
  - In the root directory of the repository on your machine run `uv build` and `uv
    tool install patkit`.
- Or you can just use `uv` to run patkit: `uv run patkit recorded_data/minimal`.
  See `uv`'s [docs](https://docs.astral.sh/uv/) for more.
  
### Using conda/mamba

[Old instructions for conda/mamba](SetupForDevelopment.markdown). These are no
longer maintained unless you want to step up and do that.

