var StoreMixin = function (store, key) {
    return {
        componentDidMount: function () {
            store.addChangeListener(this._handleStoreChange);
        },
        componentWillUnmount: function () {
            store.removeChangeListener(this._handleStoreChange);
        },
        _handleStoreChange: function () {
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
    };
};
module.exports = StoreMixin;
