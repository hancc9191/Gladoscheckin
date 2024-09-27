name: Auto Check

on:
  workflow_dispatch:
  push:
    branches: [ main ]
    paths-ignore:
      - 'README.md'
      - 'imgs/'
  schedule:
    - cron: '0 0,12 * * *'
  watch:
    types: started

jobs:
  build:
    name: Glados checkin
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8]

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install requests
    - name: running checkin
      run: |
        python checkin.py
      env:
        PUSHPLUS: ${{ secrets.PUSHPLUS }}
        COOKIES: ${{ secrets.COOKIES }}

    - name: keep alive
      uses: gautamkrishnar/keepalive-workflow@v1 # using the workflow with default settings
    - name: Delete workflow runs
      uses: Mattraks/delete-workflow-runs@v2
      with:
        token: ${{ github.token }}
        repository: ${{ github.repository }}
        retain_days: 0
        keep_minimum_runs: 10
        delete_run_by_conclusion_pattern: success
