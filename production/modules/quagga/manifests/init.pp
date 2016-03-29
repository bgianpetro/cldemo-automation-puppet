class quagga {

    service { 'quagga':
      ensure  => running
    }

    file { '/etc/quagga/daemons':
        owner   => root,
        group   => root,
        mode    => '0644',
        source => 'puppet:///modules/quagga/daemons',
        notify  => Service['quagga']
    }

    $intvars = hiera('interfaces')[$hostname]
    $networks = hiera('networks')
    file { '/etc/quagga/Quagga.conf':
        owner   => root,
        group   => root,
        mode    => '0644',
        content => template('quagga/Quagga.conf.erb'),
        notify  => Service['quagga']
    }
}
