var component = require('../lib/component');
var React = require('react');

module.exports = React.createClass({
    componentDidMount: function() {
        if (typeof window !== 'undefined') {
            var node = this.getDOMNode();
            window.jQuery('.ui.menu .item', node).tab({
                context: node,
                onTabLoad: function(tab) {
                    // Bypass setState so we don't end up in a re-render loop
                    this.props.state[this.props.attribute] = tab;
                }.bind(this)
            });
        }
    },
    componentDidUpdate: function() {
        var node = this.getDOMNode();
        window.jQuery('.ui.menu .item', node).tab('change tab', this.getTabKey());
    },
    componentWillUnmount: function() {
        var node = this.getDOMNode();
        window.jQuery('.ui.menu .item', node).tab('destroy');
    },
    getTabKey: function() {
        return this.props.state[this.props.attribute];
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

        var tabKey = this.getTabKey();

        this.props.children.forEach(function(child) {
            var active = child.key == tabKey ? "active": "";
            var item = <a key={"item-" + child.key} data-tab={child.key} className={ "item " + active }>{child.props.title}</a>;
            items.push(item);

            var tab = <div key={"tab-" + child.key} data-tab={child.key} className={ (child.key == tabKey ? "active": "") + " " + tabClassName + " tab-" + child.key }>
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
