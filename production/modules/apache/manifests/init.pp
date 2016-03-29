class apache {
    package { 'apache2':
        ensure => 'installed',
        provider => 'apt'
    }

    service { 'apache2':
        ensure     => running,
        enable     => true,
        hasrestart => true,
        hasstatus  => true,
    }
}
