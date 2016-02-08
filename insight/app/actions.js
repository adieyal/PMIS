export const LOGIN
export const LOGIN_FAILURE
export const LOGOUT

export const NOTIFY

export const RECEIVE_CLUSTER
export const RECEIVE_PROJECTS

export const SET_FINANCIAL_YEAR
export const SET_PREFERENCE

export function login(authToken) {
    return { type: LOGIN, authToken };
}

export function loginFailure(data) {
    return { type: LOGIN_FAILURE, data };
}

export function logout() {
    return { type: LOGOUT  };
}

export function notify(notification) {
    return { type: NOTIFY, notification };
}

export function receiveCluster(cluster) {
    return { type: RECEIVE_CLUSTER, cluster };
}

export function receiveProjects(projects) {
    return { type: RECEIVE_PROJECTS, projects };
}

export function setFinancialYear(year) {
    return { type: SET_FINANCIAL_YEAR, year };
}

export function setPreference(key, value) {
    return { type: SET_PREFERENCE, key, value };
}
