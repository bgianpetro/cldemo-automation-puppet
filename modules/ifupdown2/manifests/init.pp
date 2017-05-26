class ifupdown2 {

    $intvars = hiera('interfaces')[$hostname]
    file { '/etc/network/interfaces':
        owner   => root,
        group   => root,
        mode    => '0644',
        content => template('ifupdown2/interfaces.erb'),
    }

    exec { '/sbin/ifreload -a':
        subscribe   => File['/etc/network/interfaces'],
        refreshonly => true
    }
}
