USE chatbot_project;
CREATE TABLE complaints (
    complaint_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    issue TEXT NOT NULL,
    product VARCHAR(100),
    status VARCHAR(20) DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

use chatbot_project;
CREATE TABLE IF NOT EXISTS users (
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  name VARCHAR(120) NOT NULL,
  role ENUM('user','admin') DEFAULT 'user',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS user_preferences (
  user_id INT PRIMARY KEY,
  preferred_tags JSON NULL,
  color_prefs JSON NULL,
  size_prefs JSON NULL,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_pref_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS products (
  product_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  price DECIMAL(10,2) NOT NULL DEFAULT 0,
  image_url TEXT,
  inventory_qty INT NOT NULL DEFAULT 0,
  is_active TINYINT(1) NOT NULL DEFAULT 1,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS tags (
  tag_id INT AUTO_INCREMENT PRIMARY KEY,
  tag VARCHAR(64) NOT NULL UNIQUE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS product_tags (
  product_id INT NOT NULL,
  tag_id INT NOT NULL,
  PRIMARY KEY (product_id, tag_id),
  FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE,
  FOREIGN KEY (tag_id) REFERENCES tags(tag_id) ON DELETE CASCADE
) ENGINE=InnoDB;

INSERT INTO products (name, description, price, image_url, inventory_qty)
VALUES
('Handmade Teddy', 'Soft crochet teddy bear, perfect gift.', 450.00, 'https://i.pinimg.com/736x/0a/d3/38/0ad33846403dbbc03a6f8aa89660e146.jpg', 12),
('Crochet Scarf', 'Warm minimal crochet scarf.', 350.00, 'https://i.pinimg.com/736x/f6/f0/49/f6f0490e4025e5614774bb943c0535a8.jpg', 20),
('Amigurumi Keychain', 'Mini amigurumi keychain with cute details.', 150.00, 'https://i.pinimg.com/736x/33/e6/8f/33e68fa96648b49fd90bc5d01d03e494.jpg', 30),
('Handmade Teddy', 'Classic plush crochet teddy.', 450.00, 'https://i.pinimg.com/1200x/d1/0a/35/d10a35b990964fe88d446595f3bfc278.jpg', 10),
('Crochet Scarf', 'Lightweight crochet scarf for daily wear.', 350.00, 'https://i.pinimg.com/736x/49/d4/4e/49d44ee86c27da0428bfda907baa7f34.jpg', 18),
('Amigurumi Keychain', 'Handmade keychain, ideal for gifting.', 150.00, 'https://i.pinimg.com/1200x/5e/28/0c/5e280cea0e8cb794bcf425f50d2665e7.jpg', 40),
('Handmade Teddy', 'Premium yarn teddy, ultra soft.', 450.00, 'https://i.pinimg.com/736x/ef/ec/23/efec23ef2a6d772130ffd4f6ba6e9fe1.jpg', 9),
('Crochet Scarf', 'Neutral tones crochet scarf.', 350.00, 'https://i.pinimg.com/1200x/bb/4d/ce/bb4dce73122b97013c01c656ff5b8e33.jpg', 22),
('Amigurumi Keychain', 'Compact amigurumi charm.', 150.00, 'https://i.pinimg.com/1200x/b0/04/74/b0047440a961ddfb65f45ead7ba31b98.jpg', 35);

INSERT IGNORE INTO tags(tag)
VALUES ('teddy'),('amigurumi'),('keychain'),('scarf'),
       ('handmade'),('gift'),('soft'),('minimal'),
       ('cat'),('bear'),
       ('blue'),('pink'),('brown'),('neutral');

-- Teddy 1 (product_id = 1)
INSERT IGNORE INTO product_tags(product_id, tag_id)
SELECT 1, tag_id FROM tags WHERE tag IN ('teddy','handmade','soft','gift','bear','brown');

-- Scarf 2
INSERT IGNORE INTO product_tags(product_id, tag_id)
SELECT 2, tag_id FROM tags WHERE tag IN ('scarf','handmade','minimal','neutral','gift');

-- Keychain 3
INSERT IGNORE INTO product_tags(product_id, tag_id)
SELECT 3, tag_id FROM tags WHERE tag IN ('amigurumi','keychain','handmade','gift','cat','blue');

-- Teddy 4
INSERT IGNORE INTO product_tags(product_id, tag_id)
SELECT 4, tag_id FROM tags WHERE tag IN ('teddy','handmade','soft','gift','bear');

-- Scarf 5
INSERT IGNORE INTO product_tags(product_id, tag_id)
SELECT 5, tag_id FROM tags WHERE tag IN ('scarf','handmade','minimal','neutral');

-- Keychain 6
INSERT IGNORE INTO product_tags(product_id, tag_id)
SELECT 6, tag_id FROM tags WHERE tag IN ('amigurumi','keychain','handmade','gift','pink');

-- Teddy 7
INSERT IGNORE INTO product_tags(product_id, tag_id)
SELECT 7, tag_id FROM tags WHERE tag IN ('teddy','handmade','soft','gift','bear');

-- Scarf 8
INSERT IGNORE INTO product_tags(product_id, tag_id)
SELECT 8, tag_id FROM tags WHERE tag IN ('scarf','handmade','minimal','neutral','brown');

-- Keychain 9
INSERT IGNORE INTO product_tags(product_id, tag_id)
SELECT 9, tag_id FROM tags WHERE tag IN ('amigurumi','keychain','handmade','gift','blue');

CREATE TABLE IF NOT EXISTS purchases (
purchase_id INT AUTO_INCREMENT PRIMARY KEY,
user_id INT NOT NULL,
product_id INT NOT NULL,
qty INT NOT NULL,
price_at_purchase DECIMAL(10,2) NOT NULL,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
) ENGINE=InnoDB;

