# catalogue-sync-reporter
Automatically check the results for each datatset in the list.

Options:

`  -h, --help            show this help message and exit`

    --dslist            The dataset list.
    --storage           Folder to look for data.

Example:

`nohup ~/miniconda3/bin/python ~/cats_status_vbn/datasets_status.py --dslist ~/cats_status_vbn/datasets_list.txt --storage /data/eo/ > ~/cats_status_vbn/out_store03_.csv &`
