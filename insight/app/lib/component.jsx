var component = require('omniscient').withDefaults({ jsx: true });

if (false && process.env.NODE_ENV != 'production') {
    component.debug();
}

module.exports = component;
