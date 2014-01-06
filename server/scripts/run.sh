#phantomjs rasterize.js http://localhost:8000/reports/district/2/dashboard/2013/7/ gert_sibande_1.pdf A4
#phantomjs rasterize.js http://localhost:8000/reports/district/2/progress/2013/7/ gert_sibande_2.pdf A4
#phantomjs rasterize.js http://localhost:8000/reports/district/2/perform/2013/7/ gert_sibande_3.pdf A4
#phantomjs rasterize.js http://localhost:8000/reports/district/3/dashboard/2013/7/ nkangala_1.pdf A4
#phantomjs rasterize.js http://localhost:8000/reports/district/3/progress/2013/7/ nkangala_2.pdf A4
#phantomjs rasterize.js http://localhost:8000/reports/district/3/perform/2013/7/ nkangala_3.pdf A4
#phantomjs rasterize.js http://localhost:8000/reports/district/4/dashboard/2013/7/ ehalanzeni_1.pdf A4
#phantomjs rasterize.js http://localhost:8000/reports/district/4/progress/2013/7/ ehalanzeni_2.pdf A4
#phantomjs rasterize.js http://localhost:8000/reports/district/4/perform/2013/7/ ehalanzeni_3.pdf A4

phantomjs rasterize2.js http://pmis/reports/cluster/dashboard/doe/2013/10/ cluster_1.pdf A4
phantomjs rasterize2.js http://pmis/reports/cluster/progress/doe/2013/10/ cluster_2.pdf A4
phantomjs rasterize2.js http://pmis/reports/cluster/performance/doe/2013/10/ cluster_3.pdf A4
phantomjs rasterize2.js http://pmis/reports/headoffice/dashboard/2013/10/ headoffice_1.pdf A4
phantomjs rasterize2.js http://pmis/reports/headoffice/progress/2013/10/ headoffice_2.pdf A4
phantomjs rasterize2.js http://pmis/reports/headoffice/performance/2013/10/ headoffice_3.pdf A4

pdftk cluster_* cat output cluster.pdf
pdftk headoffice_* cat output headoffice.pdf
