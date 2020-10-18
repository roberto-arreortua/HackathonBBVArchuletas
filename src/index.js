const express = require('express');
const morgan = require('morgan');
const cors = require('cors');
const pkg = require('../package.json');
const voice = require('./controllers/voice.controller');


const app = express();

app.set('port', process.env.PORT || 3000);

app.use(morgan('dev'));
app.use(cors());

app.post('/enrollVoice/:customerId', voice.enrollVoice);
app.post('/verifyVoice/:customerId', voice.verifyVoice);
app.get('/', (req, res) => {
    res.json({
        Project: pkg.name,
        Autor: pkg.author,
        Description: pkg.description,
        Version: pkg.version
    });
});
app.get('*', (req, res) => { res.status(404).send('What happened?') });

app.listen(app.get('port'), () => {
    console.log(`Server live on port ${app.get('port')}.`);
});