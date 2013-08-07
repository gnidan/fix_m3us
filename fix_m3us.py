#!/usr/bin/python
# fixes m3u's and m3u8's to use relative paths instead of absolute

import sys
import os
import shutil

ALLOWED_DUPLICATES = ['.DS_Store']

def fix_m3u(m3u_path, all_files):
  # copy m3u
  shutil.copy2(m3u_path, m3u_path + '.backup')
  (m3u_path_head, _) = os.path.split(m3u_path)

  outlines = []
  fp = open(m3u_path, 'U')
  for line in fp.readlines():
    line = line.strip()
    if line.startswith('#'):
      outlines.append(line)
    else:
      (path, fname) = os.path.split(line)
      print "* fixing file: " + fname
      if fname in all_files:
        outlines.append(os.path.relpath(all_files[fname], m3u_path_head))
      elif os.path.isfile(line):
        sys.stderr.write(" * could not find file in m3u directory, copying " +
          "absolute path\n")
        new_path = m3u_path_head + "/" + fname
        shutil.copy2(line, new_path)
        outlines.append(os.path.relpath(new_path, m3u_path_head))
      else:
        sys.stderr.write("ERROR: could not find song matching: " + fname)
        sys.exit(1)
  fp.close()

  fp = open(m3u_path, 'w')
  for line in outlines:
    fp.write(line)
    fp.write('\n')
  fp.close()
  

if __name__ == '__main__':
  if len(sys.argv) > 1:
    rootdir = sys.argv[1]
  else:
    rootdir = '.'

  m3us = []
  all_files = dict()
  for root, directories, files in os.walk(rootdir):
    for fname in files:
      fname_path = root + '/' + fname
      if fname in all_files and \
          fname not in ALLOWED_DUPLICATES and \
          fname_path != all_files[fname]:
        sys.stderr.write("WARNING: multiple files with the same path ending. " +
            "tell nick to fix this to ensure things aren't broken.\n")
        sys.stderr.write("OFFENDING FILES: \n")
        sys.stderr.write("  " + fname_path + "\n")
        sys.stderr.write("  " + all_files[fname] + "\n")

      all_files[fname] = fname_path
      if fname.endswith(".m3u") or fname.endswith(".m3u8"):
        m3us.append( fname_path )
  
  for m3u in m3us:
    print "*** fixing m3u:", m3u
    fix_m3u(m3u, all_files)
