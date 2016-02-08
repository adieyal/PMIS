import { combineReducers } from 'redux'
import { } from './actions'

function auth(state = { status: 'logged-out' }, action) {
    switch(action.type) {
        case LOGIN:
            return {
                status: 'logged-in',
                authToken: action.authToken
            };
        case LOGIN_FAILURE:
            return {
                status: 'failure',
                data: action.data
            };
        case LOGOUT:
            return {
                status: 'logged-out'
            };
        default:
            return state;
    }
}

function clusters(state = {}, action) {
    switch(action.type) {
        case SET_FINANCIAL_YEAR:
            return {};
        case RECEIVE_CLUSTER:
            cluster = action.cluster;
            state[cluster.slug] = cluster;
            return state;
        default:
            return state;
    }
}

function districts(state = { districts: {}, maxProjects = 0 }, action) {
    switch(action.type) {
        case SET_FINANCIAL_YEAR:
            return {
                districts: {},
                maxProjects: 0
            };
        case RECEIVE_CLUSTER:
            cluster = action.cluster;
            state.districts[cluster.slug] = cluster.districts;
            cluster.districts.reduce(function(acc, d) {
                return Math.max(acc, d['projects-implementation']);
            }, state.maxProjects);
            return state;
        default:
            return state;
    }
}

function notifications(state = [], action) {
    switch(action.type) {
        case NOTIFY:
            state.push(action.notification);
            return state;
        default:
            return state;
    }
}

function preferences(state = { view: 'dashboard', order: 'alphabetic', year: year }) {
    switch(action.type) {
        case SET_PREFERENCE:
            state[action.key] = action.value;
            return state;
        case SET_FINANCIAL_YEAR:
            state.year = action.year;
            return state;
        default:
            return state;
    }
}

function projects(state = [], action) {
    switch(action.type) {
        case SET_FINANCIAL_YEAR:
            return [];
        case RECEIVE_PROJECTS:
            return action.projects;
        default:
            return state;
    }
}

const insightApp = combineReducers({
    auth,
    clusters,
    districts,
    notifications,
    preferences,
    projects
});

export default insightApp;
