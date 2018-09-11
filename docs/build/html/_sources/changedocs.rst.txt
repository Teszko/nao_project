
How-to: edit the docs
=====================

Docs are created using python sphinx. `Source <https://github.com/Teszko/nao_project/tree/master/docs>`_


Compile the docs
----------------

First make sure you have all the necessary dependencies installed.
From the project source::

  pip install -r requirements.txt

Change into the ``docs/`` directory. To do a full rebuild run::

  make clean
  make html

The compiled docs should now be in ``docs/build/html/``


Edit the docs
-------------

Edit the source files in ``docs/source/``. *index.rst* is the main page. If you create new pages make sure to add them to the *toctree* in *index.rst*

For information about the syntax reference `reStructuredText Markup Specification <http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html>`_


autodoc
-------

*autodoc* can be used to automatically generate the api reference. View api.rst and the autodoc `docs <http://www.sphinx-doc.org/en/stable/ext/autodoc.html>`_ for more information.
