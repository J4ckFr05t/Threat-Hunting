var createError = require('http-errors');
var express = require('express');
const fileUpload = require('express-fileupload');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var bodyParser = require('body-parser')
var morgan  = require('morgan')
var fs = require('fs')
const port = 8080

const connectDB = require('./DB/connection')
connectDB();

var indexRouter = require('./routes/index');
var usersRouter = require('./routes/users');

var app = express();

app.listen(port, () => {
  console.log(`Webserver listening on port ${port}`)
})

app.use(fileUpload());

app.use(morgan('combined', {
  stream: fs.createWriteStream(path.join(__dirname, 'access.log'), { flags: 'a' })
}))

app.use(bodyParser.urlencoded({extended: true}));
app.use(bodyParser.json());
// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');


app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));
app.use('/css',express.static(path.join(__dirname,'public/css')))
app.use('/images',express.static(path.join(__dirname,'public/images')))
app.use('/js',express.static(path.join(__dirname,'public/js')))

app.use('/', indexRouter);
app.use('/machines', usersRouter);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;
