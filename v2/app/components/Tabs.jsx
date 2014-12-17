var React = require('react');

module.exports = React.createClass({
    componentDidMount: function() {
        if (typeof window !== 'undefined') {
            var node = this.getDOMNode();
            window.jQuery('.ui.menu .item', node).tab({
                context: node
            });
        }
    },
    componentDidUpdate: function() {
        var node = this.getDOMNode();
        window.jQuery('.ui.menu .item', node).tab('change tab', this.props.tab);
    },
    componentWillUnmount: function() {
        var node = this.getDOMNode();
        window.jQuery('.ui.menu .item', node).tab('destroy');
    },
    render: function() {
        var items = [];
        var tabs = [];
        var itemsClassName;
        var tabClassName;

        if (this.props.type == 'inner') {
            itemsClassName = "ui top attached tabular menu";
            tabClassName = "ui bottom attached tab segment";
        } else {
            itemsClassName = "ui pointing secondary menu";
            tabClassName = "ui tab";
        }

        this.props.children.forEach(function(child) {
            var active = child.key == this.props.tab ? "active": "";
            var item = <a key={"item-" + child.key} data-tab={child.key} className={ "item " + active }>{child.props.title}</a>;
            items.push(item);

            var tab = <div key={"tab-" + child.key} data-tab={child.key} className={ (child.key == this.props.tab ? "active": "") + " " + tabClassName + " tab-" + child.key }>
                {child}
            </div>;
            tabs.push(tab);
        }.bind(this));

        return <div className="tabs">
            <div className={itemsClassName}>
                {items}
            </div>
            {tabs}
        </div>;
    }
});
