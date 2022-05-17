#! /usr/bin/env python
# -*- coding: utf-8 -*-
from dcdb.connector import Base
import dcdb.models
from eralchemy import render_er

if __name__ == '__main__':
    render_er(Base, 'docs/database_er_model.png')
    render_er(Base, 'docs/database_er_model.pdf')
