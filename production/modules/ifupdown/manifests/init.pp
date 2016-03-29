class ifupdown {
    file { '/etc/network/interfaces':
        owner   => root,
        group   => root,
        mode    => '0644',
        content => template('ifupdown/interfaces.erb'),
    }

    exec { '/sbin/ifdown -a && /sbin/ifup -a':
        subscribe   => File['/etc/network/interfaces'],
        refreshonly => true
    }
}
