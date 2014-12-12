module.exports = {
    colours: [
        '#1f77b4',
        '#2ca02c',
        '#ff7f0e',
        '#d62728',
        '#9467bd',
        '#8c564b',
        '#e377c2',
        '#7f7f7f',
        '#bcbd22',
        '#17becf'
    ],

    clusters: [
        { slug: "education", title: 'Education', view: "performance" },
        { slug: "health", title: 'Health', view: "performance" },
        { slug: "social-development", title: 'Social Development', view: "performance" },
        { slug: "culture-sports-science-and-recreation", title: 'Culture, Sports, Science and Recreation', view: "performance" },
        { slug: "community-safety-security-and-liaison", title: 'Community, Safety, Security and Liaison', view: "performance" },
        { slug: "economic-development-environment-and-tourism", title: 'Economic Development, Environment and Tourism', view: "performance" }
    ],

    districts: {
        ehlanzeni: 'Ehlanzeni District',
        gertsibande: 'Gert Sibande District',
        nkangala: 'Nkangala District'
    },

    projectPhases: {
        'unknown': 'Unknown',
        'planning': 'Planning',
        'implementation': 'Implementation',
        'completed': 'Completed',
        'final-accounts': 'Final accounts',
    },

    planningPhases: {
        "completed": "Planning Completed",
        "consultant-appointment": "Consultant Appt",
        "design-costing": "Design Costing",
        "documentation": "Documentation",
        "tender": "For Tender"
    },

    implementationGroups: {
        "completed": "Completed",
        "practical-completion": "Practical completion",
        "final-completion": "Final completion",
        "due-3months": "Due in 3 months"
    },
    districtSummaryGroups: {
        'financial-year': "Due in financial year",
        'three-months': "Due in 3 months",
        'this-month': "Due this month",
        'practical-completion': "Practical completion",
        'final-completion': "Final completion",
    }
};
