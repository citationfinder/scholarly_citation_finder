<h1>Evaluation</h1>

## Setup

Setup the evaluation project
```bash
$ git clone git@github.com:citationfinder/evaluation.git
$ cd evaluation/
$ git clone git@github.com:citationfinder/evaluation_data.git
```
### Get evaluation set

Copy the `ssh_config.cfg.example` file to `ssh_config.cfg` and enter the SSH user and host. Execute

```bash
$ cd evaluation_data/
$ ./get_data <evaluation_name>
```

This Bash script uses SCP to download all files from the `downloads/evaluation/<evaluation_name>` directory.

### Evaluation set structure

```bash
<evaluation_name>
  |
  |- authors.csv
  |- celery.log
  |- meta_<strategy_name>.csv
  |- <strategy_name>
  |   |- <author_id>.csv
  |   |- ...
  |
  |- ...
```

## Run Matlab script


```matlab
evaluation_name = '<evaluation_name>';

% Plot for instance the journal strategies
evaluation(evaluation_name, {'journal', ...
                             'journal-ordered', ...
                             'journal-minyear'})
```