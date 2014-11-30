var StoreMixin = function (store, key) {
    function handleStoreChange() {
        var state,
            storeState = store.getState();

        if (typeof key == 'undefined') {
            state = storeState;
        } else {
            state = {};
            state[key] = storeState;
        }

        this.setState(state);
    }

    return {
        componentDidMount: function () {
            store.addChangeListener(function () {
                return handleStoreChange.call(this);
            }.bind(this));
        },
        componentWillUnmount: function () {
            store.removeChangeListener(function () {
                return handleStoreChange.call(this);
            }.bind(this));
        },
    };
};
module.exports = StoreMixin;
