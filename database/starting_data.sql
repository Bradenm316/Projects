INSERT into `users` (`username`, `password_hash`, `email`, `first_name`, `last_name`)
VALUES ('aturing', 'b93727798b520dc10d145b53909c061f082ff14cd5f8cb4ab24c3b71bfa57d7e12e1296029be74c06a0d91ba32756f9fc978047fbe7232be67f94dfc1de9ced9', 'alan@enigma.com', 'Alan', 'Turing');

INSERT into `users` (`username`, `password_hash`, `email`, `first_name`, `last_name`)
VALUES ('dritchie', '67aff785bd17ac24448d491926ff7aadd8fa75e51a2f7a9bfc31889bad0adcd2989061a27ccd9eff9e5e31f2bc14b5c193727e116dc8dc48259acb3919171cd4', 'dennis@unix.com', 'Dennis', 'Ritchie');

INSERT into `users` (`username`, `password_hash`, `email`, `first_name`, `last_name`)
VALUES ('llamport', '9171d14954eeda4e70777c23d98e349818125cdaeb884ff97ebf8cc0a9c7778f54ce394256588148132a03ebea891e44077c659e6c0132fa87a8cf77e436ae11', 'leslie@paxos.com', 'Leslie', 'Lamport');

INSERT into `users` (`username`, `password_hash`, `email`, `first_name`, `last_name`)
VALUES ('bliskov', '1e4b9ae956cad1385cfa6fffd8323dd16c3fe18c54e6447e49bddef2138d042e84e1505a541c6ef19a5026e684b2559efd366145870a0a8d4d4173c0877f6cd2', 'barbara@thor.com', 'Barbara', 'Liskov');

-- Inventories
INSERT into `inventory` (`item_name`, `info`, `price`, `stock`, `image_url`, `category`)
VALUES ('Strawberry Covered Chocolate', 'Six layer of  chocolate cake filled with ganache then iced in strawberry buttercream. Garnished with ganache, chocolate dipped strawberries, fudge icing, chocolate pieces, and macarons.', 42.99, 6, 'static/images/strawberryCoveredChocolate.jpeg', 'Cake');

INSERT into `inventory` (`item_name`, `info`, `price`, `stock`, `image_url`, `category`)
VALUES ('Cookies & Cream', 'Three layers of chocolate and three layers of vanilla cake filled with cookies and cream mousse and iced with alternating stripes of mousse and buttercream. Coated with chocolate ganache and then garnished with sandwich cookies, chocolate bars, and chocolate pieces.', 39.99, 10, 'static/images/cookiesCreamCake.jpeg', 'Cake');

INSERT into `inventory` (`item_name`, `info`, `price`, `stock`, `image_url`, `category`)
VALUES ('Pink Vanilla Dream', 'Six layers of vanilla cake iced in soft pink buttercream icing. Garnished with raspberry macarons, vanilla wafers, meringues, and white icing drip.', 39.99, 8, 'static/images/pinkVanillaDream.jpeg', 'Cake');

INSERT into `inventory` (`item_name`, `info`, `price`, `stock`, `image_url`, `category`)
VALUES ('Cheesecake', 'Consists of a thick, creamy filling over a thinner crust', 19.99, 15, 'static/images/cheesecake.jpeg', 'Cake');

INSERT into `inventory` (`item_name`, `info`, `price`, `stock`, `image_url`, `category`)
VALUES ('Tiramisu', 'Consists of layers of sponge cake soaked in coffee and brandy or liqueur with powdered chocolate and mascarpone cheese', 25.99, 12, 'static/images/tiramisu.jpeg', 'Cake');

INSERT into `inventory` (`item_name`, `info`, `price`, `stock`, `image_url`, `category`)
VALUES ('Chocolate Fudge', 'Thick layer of chocolate cake surrounding a melted chocolate inside', 36.99, 10, 'static/images/chocolate_fudge.jpeg', 'Cake');

INSERT into `inventory` (`item_name`, `info`, `price`, `stock`, `image_url`, `category`)
VALUES ('Red Velvet', 'Consists of layers of cheesecake with red velvet flavor', 40.99, 12, 'static/images/Red-Velvet-Cheesecake.jpg', 'Cake'); 

INSERT into `inventory` (`item_name`, `info`, `price`, `stock`, `image_url`, `category`)
VALUES ('Lemon Cake', 'Vanilla cake layer with lush lemon cream cheese icing', 30.99, 45, 'static/images/lemon-cake.jpg', 'Cake');

INSERT into `inventory` (`item_name`, `info`, `price`, `stock`, `image_url`, `category`)
VALUES ('Snickers', 'chocolate cake layer with sweet peanut, caramel, and nougat', 49.99, 10, 'static/images/snickers-cake.jpg', 'Cake');

INSERT into `inventory` (`item_name`, `info`, `price`, `stock`, `image_url`, `category`)
VALUES ('Strawberry Passion', 'Layers of moist Red Velvet Cake, Strawberry Puree and Strawberry Ice Cream with Graham Cracker Pie Crust wrapped in fluffy Strawberry Frosting', 60.49, 100, 'static/images/Strawberry-Passion.jpeg', 'Cake');

-- INSERT into `inventory` (`item_name`, `info`, `price`, `stock`, `image_url`, `category`)
-- VALUES ();

INSERT into `sales` (`transaction_id`, `username`, `item_id`, `quantity`, `sale_date`, `cost`)
VALUES ('1', 'aturing', '1', 10, '2022-12-21 7:30:30', 5.50);

INSERT into `sales` (`transaction_id`, `username`, `item_id`, `quantity`, `sale_date`, `cost`)
VALUES ('2', 'dritchie', '2', 10, '2022-12-21 7:30:30', 5.50);

INSERT into `sales` (`transaction_id`, `username`, `item_id`, `quantity`, `sale_date`, `cost`)
VALUES ('3', 'llamport', '3', 10, '2022-12-21 7:30:30', 5.50);