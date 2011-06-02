CREATE TABLE IF NOT EXISTS `contato` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usuario_id` int(11) NOT NULL,
  `amigo_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

INSERT INTO `contato` (`id`, `usuario_id`, `amigo_id`) VALUES
(1, 1, 2);

CREATE TABLE IF NOT EXISTS `usuario` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `login` varchar(20) NOT NULL,
  `senha` varchar(32) NOT NULL,
  `ip` varchar(16) NOT NULL,
  `status` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

INSERT INTO `usuario` (`id`, `login`, `senha`, `ip`, `status`) VALUES
(1, 'teste', '202cb962ac59075b964b07152d234b70', '', 0),
(2, 'teste2', 'caf1a3dfb505ffed0d024130f58c5cfa', '', 0);