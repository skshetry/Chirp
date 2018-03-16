# ProjectChirp
Project Chirp is a social networking site written using Python/Django. 
See demo here: https://projectchirp.herokuapp.com/

## Installation

1. Create a postgres database named `chirp` with you as an `owner`.
2. Clone this repo(preferably use ssh clone instead of https, you won't be bothered asking for password every time you push/pull). 
   - `git clone git@github.com:skshetry/Chirp.git`
3. `cd` into this repo(where you cloned) and create a virtual environment(preferably, using `python -m venv venv` on `bash`/`zsh`).

    On Windows if above didn't work, `c:\Python36\python -m venv c:\path\to\venv`.^[[1](https://docs.python.org/3/library/venv.html)]
4. Activate the virtual environment( `source venv/bin/activate`).
   
    On Windows, either use `venv\Scripts\activate.bat` on `cmd.exe` or `venv\Scripts\Activate.ps1`on `PowerShell`(default on Windows 10).
5. Install all the requirements (`pip install -r requirements/local.txt`).

    If this didn't work, use `python -m pip install -r requirements/local.txt`.
6. Copy the file `env.example` from root of the repo in a new file `.env`(dot env) in the same directory. 
Don't delete `env.example` though.
7. Open the file and change the `<user>` to the database `owner` and  `<pass>` to the database password.
8. Make migrations file and migrate.
   - ~~`./manage.py makemigrations`~~
   - `./manage.py migrate`
9. Run test to ensure everything is working.
   - `./manage.py test`

      If it doesn't, revisit all the above points. It might be that you have forgotten something along the way.
10. Run the development server. 
   - `./manage.py runserver`
11. Open the repo in your favorite text editor.
12. Before you start working, create a issue and corresponding WIP(Work in Progress) branch and merge request(MR) from gitlab. 

Pull that using `git pull --all` and checkout to the new branch(`git checkout <branchname>`).
