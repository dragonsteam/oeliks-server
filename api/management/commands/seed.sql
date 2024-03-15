insert into
  api_section (id, name, is_active)
values
  (1, 'Children', 1),
  (2, 'Property', 1),
  (3, 'Vehicles', 1),
  (4, 'Jobs', 1),
  (5, 'Pets', 1),
  (6, 'Home', 1),
  (7, 'Gadges', 1),
  (8, 'Business', 1),
  (10, 'Magazines', 1);
  (11, 'Flowers', 1),
  (12, 'Cleaning', 1),
  (13, 'Baking', 1),
  (14, 'Beauty', 1),
  (15, 'Stationary', 1),
  (16, 'Spices', 1);

insert into
  api_category (id, name, is_active, section_id)
values
  (1, 'Toys', 1, 1),
  (2, 'Dogs', 1, 5);