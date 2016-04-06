# Any node that doesn't fit into another category will use the default node
# instead.
node default {

}

# We use the hostname to figure out what roles we should be assigning to the
# node. For leaves and spines, we can use a catch-all regular expression.
node /^leaf\d+.lab.local$/ {
    include quagga
    include ifupdown2
}

node /^spine\d+.lab.local$/ {
    include quagga
    include ifupdown2
}

# Node definitions may not overlap, so we have to define the servers separately
# since they include different modules.
node server01.lab.local {
    include ifupdown
}

node server02.lab.local {
    include ifupdown
    include apache
}
