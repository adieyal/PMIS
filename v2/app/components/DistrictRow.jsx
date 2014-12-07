var React = require("react");

var Donut = require("./Donut");
var Slider = require("./Slider");

var DistrictRow = React.createClass({
    render: function() {
        var district = this.props.district;
        var content;
        var donut = this.props.donut || 'performance';

        if (this.props.layout == 'horizontal') {
            content = <div className="ui two column grid">
                <div className="column">
                    <Donut data={district[donut]} height="200" />
                </div>
                <div className="column">
                    <Slider data={district.performance} height="170" />
                </div>
            </div>;
        } else {
            content = <div>
                <Slider data={district.performance} height="170" />
                <Donut data={district[donut]} height="200" />
            </div>;
        };
        return <div className="district-row">
            <div className="ui header">{district.title}</div>
            <div className="meta">{district.numbers.implementation} Projects in Implementation</div>
            {content}
        </div>;
    }
});

module.exports = DistrictRow;
