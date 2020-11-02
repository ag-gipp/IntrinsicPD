# This is a workaround build until all source files in this repository are up-to-date
# or the Python requirements of the plagapp are fixed.
FROM son1i/intrinsic:first
EXPOSE 5000
# It overwrites only a single image. Everything else stays the same.
COPY app/static/resources/BUW_Logo.png /plagapp/app/static/resources/BUW_Logo.png
# Command options are a copy of the FROM image.
ENTRYPOINT ["python2.7"]
CMD ["plagapp/run.py"]
