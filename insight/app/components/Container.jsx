var component = require('omniscient').withDefaults({
    jsx: true
});

component.debug();

var React = require('react');
var MetaSlider = require('./MetaSlider.jsx');
var PreferenceStruct = require('./PreferenceStruct.jsx');

var Container = component('Container', function({ preferences }) {
    return <MetaSlider
        year={preferences.get('year')}
        budget={200}
        planned={80}
        actual={45}
    />;
});

function render() {
    React.render(
        <Container preferences={PreferenceStruct.cursor()} />,
        document.body
    );
}

PreferenceStruct.on('swap', render);
render();

PreferenceStruct.cursor().set('year', 2010);
