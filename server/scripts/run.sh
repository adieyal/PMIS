#phantomjs rasterize.js http://localhost:8000/reports/district/2/dashboard/2013/7/ gert_sibande_1.pdf A4
#phantomjs rasterize.js http://localhost:8000/reports/district/2/progress/2013/7/ gert_sibande_2.pdf A4
#phantomjs rasterize.js http://localhost:8000/reports/district/2/perform/2013/7/ gert_sibande_3.pdf A4
phantomjs rasterize.js http://localhost:8000/reports/district/3/dashboard/2013/7/ nkangala_1.pdf A4
phantomjs rasterize.js http://localhost:8000/reports/district/3/progress/2013/7/ nkangala_2.pdf A4
phantomjs rasterize.js http://localhost:8000/reports/district/3/perform/2013/7/ nkangala_3.pdf A4
phantomjs rasterize.js http://localhost:8000/reports/district/4/dashboard/2013/7/ ehalanzeni_1.pdf A4
phantomjs rasterize.js http://localhost:8000/reports/district/4/progress/2013/7/ ehalanzeni_2.pdf A4
phantomjs rasterize.js http://localhost:8000/reports/district/4/perform/2013/7/ ehalanzeni_3.pdf A4

#pdftk gert_* cat output gert_sibande.pdf
pdftk nkangala_* cat output nkangala.pdf
pdftk ehlanzeni_* cat output ehlanzeni.pdf
