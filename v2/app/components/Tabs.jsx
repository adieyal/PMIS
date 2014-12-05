var React = require('react');

module.exports = React.createClass({
    initTab: function() {
        if (typeof window !== 'undefined') {
            var node = this.getDOMNode();
            window.jQuery('.ui.menu .item', node).tab({
                context: node
            });
        }
    },
    componentDidMount: function() {
        this.initTab();
    },
    componentDidUpdate: function() {
        this.initTab();
    },
    getInitialState: function() {
        return {
            view: this.props.view
        };
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
            var active = child.key == this.state.view ? "active": "";
            var item = <a key={"item-" + child.key} data-tab={child.key} className={ "item " + active }>{child.props.title}</a>;
            items.push(item);

            var tab = <div key={"tab-" + child.key} data-tab={child.key} className={ (child.key == this.state.view ? "active": "") + " " + tabClassName }>
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
