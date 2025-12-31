# NoSQL Analysis – MongoDB for FlexiMart Product Catalog

## Section A: Limitations of Relational Databases (RDBMS)

Relational databases work well when data has a fixed and uniform structure, but they struggle when product data becomes highly diverse. In FlexiMart’s case, different product categories require different attributes. For example, electronic products may require RAM, processor, and storage details, while fashion products require size, color, and material. Representing this variability in an RDBMS requires either a large number of nullable columns or multiple subtype tables, both of which increase complexity and reduce maintainability.

Frequent schema changes are another limitation. Adding a new product type or attribute in an RDBMS requires schema alterations, table redesigns, and potential downtime. This makes rapid iteration difficult in dynamic e-commerce environments. Additionally, storing customer reviews in a relational model requires multiple joins across tables, increasing query complexity and reducing performance. Nested and hierarchical data is not a natural fit for relational databases, making RDBMS less suitable for flexible product catalogs.

---

## Section B: Benefits of MongoDB (NoSQL)

MongoDB addresses these limitations through its document-oriented and schema-flexible design. Each product is stored as a JSON-like document, allowing different products to have different attributes without enforcing a rigid schema. This makes it easy to store electronics, fashion, and home appliances in the same collection while keeping only relevant fields for each product.

MongoDB also supports embedded documents, allowing customer reviews to be stored directly inside the product document. This eliminates the need for expensive joins and improves read performance when fetching product details along with reviews. Additionally, MongoDB supports horizontal scalability through sharding, making it suitable for large and growing product catalogs. New product attributes can be added without schema migrations, enabling faster development and easier adaptation to changing business requirements.

---

## Section C: Trade-offs of Using MongoDB

Despite its flexibility, MongoDB has trade-offs compared to relational databases. First, it provides weaker support for complex multi-document transactions compared to MySQL, making it less suitable for highly transactional systems like order processing. Second, data redundancy is common in document-based models, which can lead to higher storage usage and potential consistency challenges. These trade-offs mean MongoDB is better suited for flexible product catalogs rather than core transactional data.
