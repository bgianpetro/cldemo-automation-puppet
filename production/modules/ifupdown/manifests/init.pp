class ifupdown {

    $interfaces_hiera = hiera('interfaces')
    $intvars = $interfaces_hiera[$hostname]
    $networks = hiera('networks')

    file { '/etc/network/interfaces_test':
        owner   => root,
        group   => root,
        mode    => '0644',
        content => template('ifupdown/interfaces.erb'),
    }

    #exec { '/sbin/ifdown -a && /sbin/ifup -a':
    #    subscribe   => File['/etc/network/interfaces'],
    #    refreshonly => true
    #}
}
