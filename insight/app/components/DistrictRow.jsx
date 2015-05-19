var component = require('../lib/component');
var React = require("react");
var Donut = require("./Donut");
var Slider = require("./Slider");

var DistrictRow = React.createClass({
    render: function() {
        var district = this.props.district;
        var content;

        var donut = this.props.donut || 'implementation';

        if (this.props.layout == 'horizontal') {
            content = <div className="ui two column grid">
                <div className="column">
                    <Donut data={district.get(donut)} height="170" colours="districtDonutColours" />
                </div>
                <div className="column">
                    <Slider data={district.get('performance')} height="170" />
                </div>
            </div>;
        } else {
            content = <div>
                <Slider data={district.get('performance')} height="100" />
                <Donut data={district.get(donut)} height="125" colours="districtDonutColours" />
            </div>;
        };
        return <div className="district-row">
            <h4 className="ui header">{district.get('title')}</h4>
            <div className="meta">{district.get('numbers').get('implementation')} Projects in Implementation</div>
            {content}
        </div>;
    }
});

module.exports = DistrictRow;
