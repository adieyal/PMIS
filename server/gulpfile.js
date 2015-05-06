var gulp = require('gulp'),
    sass = require('gulp-sass'),
    browserSync = require('browser-sync'),
    reload = browserSync.reload;

gulp.task('styles', function() {
    return gulp.src('reports/static/css/*.scss')
        .pipe(sass())
        .pipe(gulp.dest('reports/static/css'))
        .pipe(reload({ stream: true }));
});

gulp.task('serve', [ 'default' ], function() {
    gulp.watch('reports/static/css/**/*.scss', [ 'styles' ]);
});

gulp.task('default', [ 'styles' ]);
