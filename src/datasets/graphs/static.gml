graph [
  directed 1
  name "StaticCodeGraph"
  node [
    id 0
    label "PKG::src"
    node_type "Package"
  ]
  node [
    id 1
    label "FILE::src\api\customer.js"
    node_type "File"
  ]
  node [
    id 2
    label "FILE::src\api\index.js"
    node_type "File"
  ]
  node [
    id 3
    label "FILE::src\api\middlewares\auth.js"
    node_type "File"
  ]
  node [
    id 4
    label "FILE::src\api\products.js"
    node_type "File"
  ]
  node [
    id 5
    label "FILE::src\api\shopping.js"
    node_type "File"
  ]
  node [
    id 6
    label "FILE::src\config\index.js"
    node_type "File"
  ]
  node [
    id 7
    label "FILE::src\database\connection.js"
    node_type "File"
  ]
  node [
    id 8
    label "FILE::src\database\index.js"
    node_type "File"
  ]
  node [
    id 9
    label "FILE::src\database\models\Address.js"
    node_type "File"
  ]
  node [
    id 10
    label "FILE::src\database\models\Customer.js"
    node_type "File"
  ]
  node [
    id 11
    label "FUNC::transform(doc, ret){&#13;&#10;            delete ret.password;&#13;&#10;            delete ret.salt;&#13;&#10;            delete ret.__v;&#13;&#10;        }"
    node_type "Function"
  ]
  node [
    id 12
    label "FILE::src\database\models\index.js"
    node_type "File"
  ]
  node [
    id 13
    label "FILE::src\database\models\Order.js"
    node_type "File"
  ]
  node [
    id 14
    label "FUNC::transform(doc, ret){&#13;&#10;            delete ret.__v;&#13;&#10;        }"
    node_type "Function"
  ]
  node [
    id 15
    label "FILE::src\database\models\Product.js"
    node_type "File"
  ]
  node [
    id 16
    label "FILE::src\database\repository\customer-repository.js"
    node_type "File"
  ]
  node [
    id 17
    label "FUNC::async CreateCustomer({ email, password, phone, salt }) {&#13;&#10;    try {&#13;&#10;      const customer = new CustomerModel({&#13;&#10;        email,&#13;&#10;        password,&#13;&#10;        salt,&#13;&#10;        phone,&#13;&#10;        address: [],&#13;&#10;      });&#13;&#10;      const customerResult = await customer.save();&#13;&#10;      return customerResult;&#13;&#10;    } catch (err) {&#13;&#10;      throw new APIError(&#13;&#10;        &#34;API Error&#34;,&#13;&#10;        STATUS_CODES.INTERNAL_ERROR,&#13;&#10;        &#34;Unable to Create Customer&#34;&#13;&#10;      );&#13;&#10;    }&#13;&#10;  }"
    node_type "Function"
  ]
  node [
    id 18
    label "FUNC::async CreateAddress({ _id, street, postalCode, city, country }) {&#13;&#10;    try {&#13;&#10;      const profile = await CustomerModel.findById(_id);&#13;&#10;&#13;&#10;      if (profile) {&#13;&#10;        const newAddress = new AddressModel({&#13;&#10;          street,&#13;&#10;          postalCode,&#13;&#10;          city,&#13;&#10;          country,&#13;&#10;        });&#13;&#10;&#13;&#10;        await newAddress.save();&#13;&#10;&#13;&#10;        profile.address.push(newAddress);&#13;&#10;      }&#13;&#10;&#13;&#10;      return await profile.save();&#13;&#10;    } catch (err) {&#13;&#10;      throw new APIError(&#13;&#10;        &#34;API Error&#34;,&#13;&#10;        STATUS_CODES.INTERNAL_ERROR,&#13;&#10;        &#34;Error on Create Address&#34;&#13;&#10;      );&#13;&#10;    }&#13;&#10;  }"
    node_type "Function"
  ]
  node [
    id 19
    label "FUNC::async FindCustomer({ email }) {&#13;&#10;    try {&#13;&#10;      const existingCustomer = await CustomerModel.findOne({ email: email });&#13;&#10;      return existingCustomer;&#13;&#10;    } catch (err) {&#13;&#10;      throw new APIError(&#13;&#10;        &#34;API Error&#34;,&#13;&#10;        STATUS_CODES.INTERNAL_ERROR,&#13;&#10;        &#34;Unable to Find Customer&#34;&#13;&#10;      );&#13;&#10;    }&#13;&#10;  }"
    node_type "Function"
  ]
  node [
    id 20
    label "FUNC::async FindCustomerById({ id }) {&#13;&#10;    try {&#13;&#10;      const existingCustomer = await CustomerModel.findById(id)&#13;&#10;        .populate(&#34;address&#34;)&#13;&#10;        .populate(&#34;wishlist&#34;)&#13;&#10;        .populate(&#34;orders&#34;)&#13;&#10;        .populate(&#34;cart.product&#34;);&#13;&#10;      return existingCustomer;&#13;&#10;    } catch (err) {&#13;&#10;      throw new APIError(&#13;&#10;        &#34;API Error&#34;,&#13;&#10;        STATUS_CODES.INTERNAL_ERROR,&#13;&#10;        &#34;Unable to Find Customer&#34;&#13;&#10;      );&#13;&#10;    }&#13;&#10;  }"
    node_type "Function"
  ]
  node [
    id 21
    label "FUNC::async Wishlist(customerId) {&#13;&#10;    try {&#13;&#10;      const profile = await CustomerModel.findById(customerId).populate(&#13;&#10;        &#34;wishlist&#34;&#13;&#10;      );&#13;&#10;&#13;&#10;      return profile.wishlist;&#13;&#10;    } catch (err) {&#13;&#10;      throw new APIError(&#13;&#10;        &#34;API Error&#34;,&#13;&#10;        STATUS_CODES.INTERNAL_ERROR,&#13;&#10;        &#34;Unable to Get Wishlist &#34;&#13;&#10;      );&#13;&#10;    }&#13;&#10;  }"
    node_type "Function"
  ]
  node [
    id 22
    label "FUNC::async AddWishlistItem(customerId, product) {&#13;&#10;    try {&#13;&#10;      const profile = await CustomerModel.findById(customerId).populate(&#13;&#10;        &#34;wishlist&#34;&#13;&#10;      );&#13;&#10;&#13;&#10;      if (profile) {&#13;&#10;        let wishlist = profile.wishlist;&#13;&#10;&#13;&#10;        if (wishlist.length > 0) {&#13;&#10;          let isExist = false;&#13;&#10;          wishlist.map((item) => {&#13;&#10;            if (item._id.toString() === product._id.toString()) {&#13;&#10;              const index = wishlist.indexOf(item);&#13;&#10;              wishlist.splice(index, 1);&#13;&#10;              isExist = true;&#13;&#10;            }&#13;&#10;          });&#13;&#10;&#13;&#10;          if (!isExist) {&#13;&#10;            wishlist.push(product);&#13;&#10;          }&#13;&#10;        } else {&#13;&#10;          wishlist.push(product);&#13;&#10;        }&#13;&#10;&#13;&#10;        profile.wishlist = wishlist;&#13;&#10;      }&#13;&#10;&#13;&#10;      const profileResult = await profile.save();&#13;&#10;&#13;&#10;      return profileResult.wishlist;&#13;&#10;    } catch (err) {&#13;&#10;      throw new APIError(&#13;&#10;        &#34;API Error&#34;,&#13;&#10;        STATUS_CODES.INTERNAL_ERROR,&#13;&#10;        &#34;Unable to Add to WishList&#34;&#13;&#10;      );&#13;&#10;    }&#13;&#10;  }"
    node_type "Function"
  ]
  node [
    id 23
    label "FUNC::async AddCartItem(customerId, product, qty, isRemove) {&#13;&#10;    try {&#13;&#10;      const profile = await CustomerModel.findById(customerId).populate(&#13;&#10;        &#34;cart.product&#34;&#13;&#10;      );&#13;&#10;&#13;&#10;      if (profile) {&#13;&#10;        const cartItem = {&#13;&#10;          product,&#13;&#10;          unit: qty,&#13;&#10;        };&#13;&#10;&#13;&#10;        let cartItems = profile.cart;&#13;&#10;&#13;&#10;        if (cartItems.length > 0) {&#13;&#10;          let isExist = false;&#13;&#10;          cartItems.map((item) => {&#13;&#10;            if (item.product._id.toString() === product._id.toString()) {&#13;&#10;              if (isRemove) {&#13;&#10;                cartItems.splice(cartItems.indexOf(item), 1);&#13;&#10;              } else {&#13;&#10;                item.unit = qty;&#13;&#10;              }&#13;&#10;              isExist = true;&#13;&#10;            }&#13;&#10;          });&#13;&#10;&#13;&#10;          if (!isExist) {&#13;&#10;            cartItems.push(cartItem);&#13;&#10;          }&#13;&#10;        } else {&#13;&#10;          cartItems.push(cartItem);&#13;&#10;        }&#13;&#10;&#13;&#10;        profile.cart = cartItems;&#13;&#10;&#13;&#10;        const cartSaveResult = await profile.save();&#13;&#10;&#13;&#10;        return cartSaveResult.cart;&#13;&#10;      }&#13;&#10;&#13;&#10;      throw new Error(&#34;Unable to add to cart!&#34;);&#13;&#10;    } catch (err) {&#13;&#10;      throw new APIError(&#13;&#10;        &#34;API Error&#34;,&#13;&#10;        STATUS_CODES.INTERNAL_ERROR,&#13;&#10;        &#34;Unable to Create Customer&#34;&#13;&#10;      );&#13;&#10;    }&#13;&#10;  }"
    node_type "Function"
  ]
  node [
    id 24
    label "FUNC::async AddOrderToProfile(customerId, order) {&#13;&#10;    try {&#13;&#10;      const profile = await CustomerModel.findById(customerId);&#13;&#10;&#13;&#10;      if (profile) {&#13;&#10;        if (profile.orders == undefined) {&#13;&#10;          profile.orders = [];&#13;&#10;        }&#13;&#10;        profile.orders.push(order);&#13;&#10;&#13;&#10;        profile.cart = [];&#13;&#10;&#13;&#10;        const profileResult = await profile.save();&#13;&#10;&#13;&#10;        return profileResult;&#13;&#10;      }&#13;&#10;&#13;&#10;      throw new Error(&#34;Unable to add to order!&#34;);&#13;&#10;    } catch (err) {&#13;&#10;      throw new APIError(&#13;&#10;        &#34;API Error&#34;,&#13;&#10;        STATUS_CODES.INTERNAL_ERROR,&#13;&#10;        &#34;Unable to Create Customer&#34;&#13;&#10;      );&#13;&#10;    }&#13;&#10;  }"
    node_type "Function"
  ]
  node [
    id 25
    label "FILE::src\database\repository\product-repository.js"
    node_type "File"
  ]
  node [
    id 26
    label "FUNC::async CreateProduct({&#13;&#10;    name,&#13;&#10;    desc,&#13;&#10;    type,&#13;&#10;    unit,&#13;&#10;    price,&#13;&#10;    available,&#13;&#10;    suplier,&#13;&#10;    banner,&#13;&#10;  }) {&#13;&#10;    try {&#13;&#10;      const product = new ProductModel({&#13;&#10;        name,&#13;&#10;        desc,&#13;&#10;        type,&#13;&#10;        unit,&#13;&#10;        price,&#13;&#10;        available,&#13;&#10;        suplier,&#13;&#10;        banner,&#13;&#10;      });&#13;&#10;&#13;&#10;      const productResult = await product.save();&#13;&#10;      return productResult;&#13;&#10;    } catch (err) {&#13;&#10;      throw new APIError(&#13;&#10;        &#34;API Error&#34;,&#13;&#10;        STATUS_CODES.INTERNAL_ERROR,&#13;&#10;        &#34;Unable to Create Product&#34;&#13;&#10;      );&#13;&#10;    }&#13;&#10;  }"
    node_type "Function"
  ]
  node [
    id 27
    label "FUNC::async Products() {&#13;&#10;    try {&#13;&#10;      return await ProductModel.find();&#13;&#10;    } catch (err) {&#13;&#10;      throw new APIError(&#13;&#10;        &#34;API Error&#34;,&#13;&#10;        STATUS_CODES.INTERNAL_ERROR,&#13;&#10;        &#34;Unable to Get Products&#34;&#13;&#10;      );&#13;&#10;    }&#13;&#10;  }"
    node_type "Function"
  ]
  node [
    id 28
    label "FUNC::async FindById(id) {&#13;&#10;    try {&#13;&#10;      return await ProductModel.findById(id);&#13;&#10;    } catch (err) {&#13;&#10;      throw new APIError(&#13;&#10;        &#34;API Error&#34;,&#13;&#10;        STATUS_CODES.INTERNAL_ERROR,&#13;&#10;        &#34;Unable to Find Product&#34;&#13;&#10;      );&#13;&#10;    }&#13;&#10;  }"
    node_type "Function"
  ]
  node [
    id 29
    label "FUNC::async FindByCategory(category) {&#13;&#10;    try {&#13;&#10;      const products = await ProductModel.find({ type: category });&#13;&#10;      return products;&#13;&#10;    } catch (err) {&#13;&#10;      throw new APIError(&#13;&#10;        &#34;API Error&#34;,&#13;&#10;        STATUS_CODES.INTERNAL_ERROR,&#13;&#10;        &#34;Unable to Find Category&#34;&#13;&#10;      );&#13;&#10;    }&#13;&#10;  }"
    node_type "Function"
  ]
  node [
    id 30
    label "FUNC::async FindSelectedProducts(selectedIds) {&#13;&#10;    try {&#13;&#10;      const products = await ProductModel.find()&#13;&#10;        .where(&#34;_id&#34;)&#13;&#10;        .in(selectedIds.map((_id) => _id))&#13;&#10;        .exec();&#13;&#10;      return products;&#13;&#10;    } catch (err) {&#13;&#10;      throw new APIError(&#13;&#10;        &#34;API Error&#34;,&#13;&#10;        STATUS_CODES.INTERNAL_ERROR,&#13;&#10;        &#34;Unable to Find Product&#34;&#13;&#10;      );&#13;&#10;    }&#13;&#10;  }"
    node_type "Function"
  ]
  node [
    id 31
    label "FILE::src\database\repository\shopping-repository.js"
    node_type "File"
  ]
  node [
    id 32
    label "FUNC::async Orders(customerId){&#13;&#10;        try{&#13;&#10;            const orders = await OrderModel.find({customerId }).populate('items.product');        &#13;&#10;            return orders;&#13;&#10;        }catch(err){&#13;&#10;            throw APIError('API Error', STATUS_CODES.INTERNAL_ERROR, 'Unable to Find Orders')&#13;&#10;        }&#13;&#10;    }"
    node_type "Function"
  ]
  node [
    id 33
    label "FUNC::async CreateNewOrder(customerId, txnId){&#13;&#10;&#13;&#10;        //check transaction for payment Status&#13;&#10;        &#13;&#10;        try{&#13;&#10;            const profile = await CustomerModel.findById(customerId).populate('cart.product');&#13;&#10;    &#13;&#10;            if(profile){&#13;&#10;                &#13;&#10;                let amount = 0;   &#13;&#10;    &#13;&#10;                let cartItems = profile.cart;&#13;&#10;    &#13;&#10;                if(cartItems.length > 0){&#13;&#10;                    //process Order&#13;&#10;                    cartItems.map(item => {&#13;&#10;                        amount += parseInt(item.product.price) *  parseInt(item.unit);   &#13;&#10;                    });&#13;&#10;        &#13;&#10;                    const orderId = uuidv4();&#13;&#10;        &#13;&#10;                    const order = new OrderModel({&#13;&#10;                        orderId,&#13;&#10;                        customerId,&#13;&#10;                        amount,&#13;&#10;                        txnId,&#13;&#10;                        status: 'received',&#13;&#10;                        items: cartItems&#13;&#10;                    })&#13;&#10;        &#13;&#10;                    profile.cart = [];&#13;&#10;                    &#13;&#10;                    order.populate('items.product').execPopulate();&#13;&#10;                    const orderResult = await order.save();&#13;&#10;                   &#13;&#10;                    profile.orders.push(orderResult);&#13;&#10;    &#13;&#10;                    await profile.save();&#13;&#10;    &#13;&#10;                    return orderResult;&#13;&#10;                }&#13;&#10;            }&#13;&#10;    &#13;&#10;          return {}&#13;&#10;&#13;&#10;        }catch(err){&#13;&#10;            throw APIError('API Error', STATUS_CODES.INTERNAL_ERROR, 'Unable to Find Category')&#13;&#10;        }&#13;&#10;        &#13;&#10;&#13;&#10;    }"
    node_type "Function"
  ]
  node [
    id 34
    label "FILE::src\express-app.js"
    node_type "File"
  ]
  node [
    id 35
    label "FILE::src\index.js"
    node_type "File"
  ]
  node [
    id 36
    label "FILE::src\run-parser.js"
    node_type "File"
  ]
  node [
    id 37
    label "FUNC::function toJSON(node) {&#13;&#10;    return {&#13;&#10;        type: node.type,&#13;&#10;        value: node.text,&#13;&#10;        startIndex: node.startIndex,&#13;&#10;        endIndex: node.endIndex,&#13;&#10;        startPosition: node.startPosition,&#13;&#10;        endPosition: node.endPosition,&#13;&#10;        children: node.children.map(child => toJSON(child))  // IMPORTANT FIX&#13;&#10;    };&#13;&#10;}"
    node_type "Function"
  ]
  node [
    id 38
    label "FUNC::function walk(dir, fileList = []) {&#13;&#10;    if (!fs.existsSync(dir)) return fileList;&#13;&#10;    const files = fs.readdirSync(dir);&#13;&#10;    files.forEach(f => {&#13;&#10;        const filePath = path.join(dir, f);&#13;&#10;        if (fs.lstatSync(filePath).isDirectory()) {&#13;&#10;            walk(filePath, fileList);&#13;&#10;        } else if (f.endsWith(&#34;.js&#34;)) {&#13;&#10;            fileList.push(filePath);&#13;&#10;        }&#13;&#10;    });&#13;&#10;    return fileList;&#13;&#10;}"
    node_type "Function"
  ]
  node [
    id 39
    label "FUNC::async function run() {&#13;&#10;    const parser = new Parser();&#13;&#10;    parser.setLanguage(JavaScript);&#13;&#10;&#13;&#10;    if (!JavaScript) {&#13;&#10;        console.error(&#34;&#10060; Tree-sitter JavaScript language failed to load!&#34;);&#13;&#10;        process.exit(1);&#13;&#10;    }&#13;&#10;&#13;&#10;    const foldersToScan = [&#34;src&#34;, &#34;api&#34;, &#34;routes&#34;, &#34;middleware&#34;];&#13;&#10;    let jsFiles = [];&#13;&#10;&#13;&#10;    foldersToScan.forEach(folder => {&#13;&#10;        jsFiles.push(...walk(path.join(projectRoot, folder)));&#13;&#10;    });&#13;&#10;&#13;&#10;    const results = [];&#13;&#10;&#13;&#10;    for (const file of jsFiles) {&#13;&#10;        const code = fs.readFileSync(file, &#34;utf8&#34;);&#13;&#10;        const tree = parser.parse(code);&#13;&#10;&#13;&#10;        results.push({&#13;&#10;            file: path.relative(projectRoot, file),&#13;&#10;            ast: toJSON(tree.rootNode)&#13;&#10;        });&#13;&#10;    }&#13;&#10;&#13;&#10;    const outputDir = path.join(projectRoot, &#34;src/datasets/annotations&#34;);&#13;&#10;    if (!fs.existsSync(outputDir)) {&#13;&#10;        fs.mkdirSync(outputDir, { recursive: true });&#13;&#10;    }&#13;&#10;&#13;&#10;    console.log(&#34;OUTPUT DIRECTORY:&#34;, outputDir);&#13;&#10;console.log(&#13;&#10;    &#34;FULL FILE PATH:&#34;,&#13;&#10;    path.join(outputDir, &#34;api-sementics.json&#34;)&#13;&#10;);&#13;&#10;&#13;&#10;&#13;&#10;    fs.writeFileSync(&#13;&#10;        path.join(outputDir, &#34;api-sementics.json&#34;),&#13;&#10;        JSON.stringify(results, null, 2)&#13;&#10;    );&#13;&#10;&#13;&#10;    console.log(&#34;api-sementics.json generated successfully.&#34;);&#13;&#10;}"
    node_type "Function"
  ]
  node [
    id 40
    label "FILE::src\services\customer-service.js"
    node_type "File"
  ]
  node [
    id 41
    label "FUNC::constructor(){&#13;&#10;        this.repository = new CustomerRepository();&#13;&#10;    }"
    node_type "Function"
  ]
  node [
    id 42
    label "FUNC::async SignIn(userInputs){&#13;&#10;&#13;&#10;        const { email, password } = userInputs;&#13;&#10;        &#13;&#10;        try {&#13;&#10;            &#13;&#10;            const existingCustomer = await this.repository.FindCustomer({ email});&#13;&#10;&#13;&#10;            if(existingCustomer){&#13;&#10;            &#13;&#10;                const validPassword = await ValidatePassword(password, existingCustomer.password, existingCustomer.salt);&#13;&#10;                &#13;&#10;                if(validPassword){&#13;&#10;                    const token = await GenerateSignature({ email: existingCustomer.email, _id: existingCustomer._id});&#13;&#10;                    return FormateData({id: existingCustomer._id, token });&#13;&#10;                } &#13;&#10;            }&#13;&#10;    &#13;&#10;            return FormateData(null);&#13;&#10;&#13;&#10;        } catch (err) {&#13;&#10;            throw new APIError('Data Not found', err)&#13;&#10;        }&#13;&#10;&#13;&#10;       &#13;&#10;    }"
    node_type "Function"
  ]
  node [
    id 43
    label "FUNC::async SignUp(userInputs){&#13;&#10;        &#13;&#10;        const { email, password, phone } = userInputs;&#13;&#10;        &#13;&#10;        try{&#13;&#10;            // create salt&#13;&#10;            let salt = await GenerateSalt();&#13;&#10;            &#13;&#10;            let userPassword = await GeneratePassword(password, salt);&#13;&#10;            &#13;&#10;            const existingCustomer = await this.repository.CreateCustomer({ email, password: userPassword, phone, salt});&#13;&#10;            &#13;&#10;            const token = await GenerateSignature({ email: email, _id: existingCustomer._id});&#13;&#10;&#13;&#10;            return FormateData({id: existingCustomer._id, token });&#13;&#10;&#13;&#10;        }catch(err){&#13;&#10;            throw new APIError('Data Not found', err)&#13;&#10;        }&#13;&#10;&#13;&#10;    }"
    node_type "Function"
  ]
  node [
    id 44
    label "FUNC::async AddNewAddress(_id,userInputs){&#13;&#10;        &#13;&#10;        const { street, postalCode, city,country} = userInputs;&#13;&#10;        &#13;&#10;        try {&#13;&#10;            const addressResult = await this.repository.CreateAddress({ _id, street, postalCode, city,country})&#13;&#10;            return FormateData(addressResult);&#13;&#10;            &#13;&#10;        } catch (err) {&#13;&#10;            throw new APIError('Data Not found', err)&#13;&#10;        }&#13;&#10;        &#13;&#10;    &#13;&#10;    }"
    node_type "Function"
  ]
  node [
    id 45
    label "FUNC::async GetProfile(id){&#13;&#10;&#13;&#10;        try {&#13;&#10;            const existingCustomer = await this.repository.FindCustomerById({id});&#13;&#10;            return FormateData(existingCustomer);&#13;&#10;            &#13;&#10;        } catch (err) {&#13;&#10;            throw new APIError('Data Not found', err)&#13;&#10;        }&#13;&#10;    }"
    node_type "Function"
  ]
  node [
    id 46
    label "FUNC::async GetShopingDetails(id){&#13;&#10;&#13;&#10;        try {&#13;&#10;            const existingCustomer = await this.repository.FindCustomerById({id});&#13;&#10;    &#13;&#10;            if(existingCustomer){&#13;&#10;               return FormateData(existingCustomer);&#13;&#10;            }       &#13;&#10;            return FormateData({ msg: 'Error'});&#13;&#10;            &#13;&#10;        } catch (err) {&#13;&#10;            throw new APIError('Data Not found', err)&#13;&#10;        }&#13;&#10;    }"
    node_type "Function"
  ]
  node [
    id 47
    label "FUNC::async GetWishList(customerId){&#13;&#10;&#13;&#10;        try {&#13;&#10;            const wishListItems = await this.repository.Wishlist(customerId);&#13;&#10;            return FormateData(wishListItems);&#13;&#10;        } catch (err) {&#13;&#10;            throw new APIError('Data Not found', err)           &#13;&#10;        }&#13;&#10;    }"
    node_type "Function"
  ]
  node [
    id 48
    label "FUNC::async AddToWishlist(customerId, product){&#13;&#10;        try {&#13;&#10;            const wishlistResult = await this.repository.AddWishlistItem(customerId, product);        &#13;&#10;           return FormateData(wishlistResult);&#13;&#10;    &#13;&#10;        } catch (err) {&#13;&#10;            throw new APIError('Data Not found', err)&#13;&#10;        }&#13;&#10;    }"
    node_type "Function"
  ]
  node [
    id 49
    label "FUNC::async ManageCart(customerId, product, qty, isRemove){&#13;&#10;        try {&#13;&#10;            const cartResult = await this.repository.AddCartItem(customerId, product, qty, isRemove);        &#13;&#10;            return FormateData(cartResult);&#13;&#10;        } catch (err) {&#13;&#10;            throw new APIError('Data Not found', err)&#13;&#10;        }&#13;&#10;    }"
    node_type "Function"
  ]
  node [
    id 50
    label "FUNC::async ManageOrder(customerId, order){&#13;&#10;        try {&#13;&#10;            const orderResult = await this.repository.AddOrderToProfile(customerId, order);&#13;&#10;            return FormateData(orderResult);&#13;&#10;        } catch (err) {&#13;&#10;            throw new APIError('Data Not found', err)&#13;&#10;        }&#13;&#10;    }"
    node_type "Function"
  ]
  node [
    id 51
    label "FUNC::async SubscribeEvents(payload){&#13;&#10; &#13;&#10;        const { event, data } =  payload;&#13;&#10;&#13;&#10;        const { userId, product, order, qty } = data;&#13;&#10;&#13;&#10;        switch(event){&#13;&#10;            case 'ADD_TO_WISHLIST':&#13;&#10;            case 'REMOVE_FROM_WISHLIST':&#13;&#10;                this.AddToWishlist(userId,product)&#13;&#10;                break;&#13;&#10;            case 'ADD_TO_CART':&#13;&#10;                this.ManageCart(userId,product, qty, false);&#13;&#10;                break;&#13;&#10;            case 'REMOVE_FROM_CART':&#13;&#10;                this.ManageCart(userId,product,qty, true);&#13;&#10;                break;&#13;&#10;            case 'CREATE_ORDER':&#13;&#10;                this.ManageOrder(userId,order);&#13;&#10;                break;&#13;&#10;            default:&#13;&#10;                break;&#13;&#10;        }&#13;&#10; &#13;&#10;    }"
    node_type "Function"
  ]
  node [
    id 52
    label "FILE::src\services\product-service.js"
    node_type "File"
  ]
  node [
    id 53
    label "FUNC::constructor(){&#13;&#10;        this.repository = new ProductRepository();&#13;&#10;    }"
    node_type "Function"
  ]
  node [
    id 54
    label "FUNC::async CreateProduct(productInputs){&#13;&#10;        try{&#13;&#10;            const productResult = await this.repository.CreateProduct(productInputs)&#13;&#10;            return FormateData(productResult);&#13;&#10;        }catch(err){&#13;&#10;            throw new APIError('Data Not found')&#13;&#10;        }&#13;&#10;    }"
    node_type "Function"
  ]
  node [
    id 55
    label "FUNC::async GetProducts(){&#13;&#10;        try{&#13;&#10;            const products = await this.repository.Products();&#13;&#10;    &#13;&#10;            let categories = {};&#13;&#10;    &#13;&#10;            products.map(({ type }) => {&#13;&#10;                categories[type] = type;&#13;&#10;            });&#13;&#10;            &#13;&#10;            return FormateData({&#13;&#10;                products,&#13;&#10;                categories:  Object.keys(categories) ,&#13;&#10;            })&#13;&#10;&#13;&#10;        }catch(err){&#13;&#10;            throw new APIError('Data Not found')&#13;&#10;        }&#13;&#10;    }"
    node_type "Function"
  ]
  node [
    id 56
    label "FUNC::async GetProductDescription(productId){&#13;&#10;        try {&#13;&#10;            const product = await this.repository.FindById(productId);&#13;&#10;            return FormateData(product)&#13;&#10;        } catch (err) {&#13;&#10;            throw new APIError('Data Not found')&#13;&#10;        }&#13;&#10;    }"
    node_type "Function"
  ]
  node [
    id 57
    label "FUNC::async GetProductsByCategory(category){&#13;&#10;        try {&#13;&#10;            const products = await this.repository.FindByCategory(category);&#13;&#10;            return FormateData(products)&#13;&#10;        } catch (err) {&#13;&#10;            throw new APIError('Data Not found')&#13;&#10;        }&#13;&#10;&#13;&#10;    }"
    node_type "Function"
  ]
  node [
    id 58
    label "FUNC::async GetSelectedProducts(selectedIds){&#13;&#10;        try {&#13;&#10;            const products = await this.repository.FindSelectedProducts(selectedIds);&#13;&#10;            return FormateData(products);&#13;&#10;        } catch (err) {&#13;&#10;            throw new APIError('Data Not found')&#13;&#10;        }&#13;&#10;    }"
    node_type "Function"
  ]
  node [
    id 59
    label "FUNC::async GetProductById(productId){&#13;&#10;        try {&#13;&#10;            return await this.repository.FindById(productId);&#13;&#10;        } catch (err) {&#13;&#10;            throw new APIError('Data Not found')&#13;&#10;        }&#13;&#10;    }"
    node_type "Function"
  ]
  node [
    id 60
    label "FILE::src\services\shopping-service.js"
    node_type "File"
  ]
  node [
    id 61
    label "FUNC::constructor() {&#13;&#10;    this.repository = new ShoppingRepository();&#13;&#10;  }"
    node_type "Function"
  ]
  node [
    id 62
    label "FUNC::async PlaceOrder(userInput) {&#13;&#10;    const { _id, txnNumber } = userInput;&#13;&#10;&#13;&#10;    // Verify the txn number with payment logs&#13;&#10;&#13;&#10;    try {&#13;&#10;      const orderResult = await this.repository.CreateNewOrder(_id, txnNumber);&#13;&#10;      return FormateData(orderResult);&#13;&#10;    } catch (err) {&#13;&#10;      throw new APIError(&#34;Data Not found&#34;, err);&#13;&#10;    }&#13;&#10;  }"
    node_type "Function"
  ]
  node [
    id 63
    label "FUNC::async GetOrders(customerId) {&#13;&#10;    try {&#13;&#10;      const orders = await this.repository.Orders(customerId);&#13;&#10;      return FormateData(orders);&#13;&#10;    } catch (err) {&#13;&#10;      throw new APIError(&#34;Data Not found&#34;, err);&#13;&#10;    }&#13;&#10;  }"
    node_type "Function"
  ]
  node [
    id 64
    label "FILE::src\utils\app-errors.js"
    node_type "File"
  ]
  node [
    id 65
    label "FUNC::constructor(&#13;&#10;    name,&#13;&#10;    statusCode,&#13;&#10;    description,&#13;&#10;    isOperational,&#13;&#10;    errorStack,&#13;&#10;    logingErrorResponse&#13;&#10;  ) {&#13;&#10;    super(description);&#13;&#10;    Object.setPrototypeOf(this, new.target.prototype);&#13;&#10;    this.name = name;&#13;&#10;    this.statusCode = statusCode;&#13;&#10;    this.isOperational = isOperational;&#13;&#10;    this.errorStack = errorStack;&#13;&#10;    this.logError = logingErrorResponse;&#13;&#10;    Error.captureStackTrace(this);&#13;&#10;  }"
    node_type "Function"
  ]
  node [
    id 66
    label "FUNC::constructor(&#13;&#10;    name,&#13;&#10;    statusCode = STATUS_CODES.INTERNAL_ERROR,&#13;&#10;    description = &#34;Internal Server Error&#34;,&#13;&#10;    isOperational = true&#13;&#10;  ) {&#13;&#10;    super(name, statusCode, description, isOperational);&#13;&#10;  }"
    node_type "Function"
  ]
  node [
    id 67
    label "FUNC::constructor(description = &#34;Bad request&#34;, logingErrorResponse) {&#13;&#10;    super(&#13;&#10;      &#34;NOT FOUND&#34;,&#13;&#10;      STATUS_CODES.BAD_REQUEST,&#13;&#10;      description,&#13;&#10;      true,&#13;&#10;      false,&#13;&#10;      logingErrorResponse&#13;&#10;    );&#13;&#10;  }"
    node_type "Function"
  ]
  node [
    id 68
    label "FUNC::constructor(description = &#34;Validation Error&#34;, errorStack) {&#13;&#10;    super(&#13;&#10;      &#34;BAD REQUEST&#34;,&#13;&#10;      STATUS_CODES.BAD_REQUEST,&#13;&#10;      description,&#13;&#10;      true,&#13;&#10;      errorStack&#13;&#10;    );&#13;&#10;  }"
    node_type "Function"
  ]
  node [
    id 69
    label "FILE::src\utils\error-handler.js"
    node_type "File"
  ]
  node [
    id 70
    label "FUNC::constructor(){}"
    node_type "Function"
  ]
  node [
    id 71
    label "FUNC::async logError(err){&#13;&#10;        console.log('==================== Start Error Logger ===============');&#13;&#10;        LogErrors.log({&#13;&#10;            private: true,&#13;&#10;            level: 'error',&#13;&#10;            message: `${new Date()}-${JSON.stringify(err)}`&#13;&#10;          });&#13;&#10;        console.log('==================== End Error Logger ===============');&#13;&#10;        // log error with Logger plugins&#13;&#10;      &#13;&#10;        return false;&#13;&#10;    }"
    node_type "Function"
  ]
  node [
    id 72
    label "FUNC::isTrustError(error){&#13;&#10;        if(error instanceof AppError){&#13;&#10;            return error.isOperational;&#13;&#10;        }else{&#13;&#10;            return false;&#13;&#10;        }&#13;&#10;    }"
    node_type "Function"
  ]
  node [
    id 73
    label "FILE::src\utils\index.js"
    node_type "File"
  ]
  edge [
    source 0
    target 1
    relation "CONTAINS"
  ]
  edge [
    source 0
    target 2
    relation "CONTAINS"
  ]
  edge [
    source 0
    target 3
    relation "CONTAINS"
  ]
  edge [
    source 0
    target 4
    relation "CONTAINS"
  ]
  edge [
    source 0
    target 5
    relation "CONTAINS"
  ]
  edge [
    source 0
    target 6
    relation "CONTAINS"
  ]
  edge [
    source 0
    target 7
    relation "CONTAINS"
  ]
  edge [
    source 0
    target 8
    relation "CONTAINS"
  ]
  edge [
    source 0
    target 9
    relation "CONTAINS"
  ]
  edge [
    source 0
    target 10
    relation "CONTAINS"
  ]
  edge [
    source 0
    target 12
    relation "CONTAINS"
  ]
  edge [
    source 0
    target 13
    relation "CONTAINS"
  ]
  edge [
    source 0
    target 15
    relation "CONTAINS"
  ]
  edge [
    source 0
    target 16
    relation "CONTAINS"
  ]
  edge [
    source 0
    target 25
    relation "CONTAINS"
  ]
  edge [
    source 0
    target 31
    relation "CONTAINS"
  ]
  edge [
    source 0
    target 34
    relation "CONTAINS"
  ]
  edge [
    source 0
    target 35
    relation "CONTAINS"
  ]
  edge [
    source 0
    target 36
    relation "CONTAINS"
  ]
  edge [
    source 0
    target 40
    relation "CONTAINS"
  ]
  edge [
    source 0
    target 52
    relation "CONTAINS"
  ]
  edge [
    source 0
    target 60
    relation "CONTAINS"
  ]
  edge [
    source 0
    target 64
    relation "CONTAINS"
  ]
  edge [
    source 0
    target 69
    relation "CONTAINS"
  ]
  edge [
    source 0
    target 73
    relation "CONTAINS"
  ]
  edge [
    source 10
    target 11
    relation "HAS_FUNCTION"
  ]
  edge [
    source 13
    target 14
    relation "HAS_FUNCTION"
  ]
  edge [
    source 16
    target 17
    relation "HAS_FUNCTION"
  ]
  edge [
    source 16
    target 18
    relation "HAS_FUNCTION"
  ]
  edge [
    source 16
    target 19
    relation "HAS_FUNCTION"
  ]
  edge [
    source 16
    target 20
    relation "HAS_FUNCTION"
  ]
  edge [
    source 16
    target 21
    relation "HAS_FUNCTION"
  ]
  edge [
    source 16
    target 22
    relation "HAS_FUNCTION"
  ]
  edge [
    source 16
    target 23
    relation "HAS_FUNCTION"
  ]
  edge [
    source 16
    target 24
    relation "HAS_FUNCTION"
  ]
  edge [
    source 25
    target 26
    relation "HAS_FUNCTION"
  ]
  edge [
    source 25
    target 27
    relation "HAS_FUNCTION"
  ]
  edge [
    source 25
    target 28
    relation "HAS_FUNCTION"
  ]
  edge [
    source 25
    target 29
    relation "HAS_FUNCTION"
  ]
  edge [
    source 25
    target 30
    relation "HAS_FUNCTION"
  ]
  edge [
    source 31
    target 32
    relation "HAS_FUNCTION"
  ]
  edge [
    source 31
    target 33
    relation "HAS_FUNCTION"
  ]
  edge [
    source 36
    target 37
    relation "HAS_FUNCTION"
  ]
  edge [
    source 36
    target 38
    relation "HAS_FUNCTION"
  ]
  edge [
    source 36
    target 39
    relation "HAS_FUNCTION"
  ]
  edge [
    source 40
    target 41
    relation "HAS_FUNCTION"
  ]
  edge [
    source 40
    target 42
    relation "HAS_FUNCTION"
  ]
  edge [
    source 40
    target 43
    relation "HAS_FUNCTION"
  ]
  edge [
    source 40
    target 44
    relation "HAS_FUNCTION"
  ]
  edge [
    source 40
    target 45
    relation "HAS_FUNCTION"
  ]
  edge [
    source 40
    target 46
    relation "HAS_FUNCTION"
  ]
  edge [
    source 40
    target 47
    relation "HAS_FUNCTION"
  ]
  edge [
    source 40
    target 48
    relation "HAS_FUNCTION"
  ]
  edge [
    source 40
    target 49
    relation "HAS_FUNCTION"
  ]
  edge [
    source 40
    target 50
    relation "HAS_FUNCTION"
  ]
  edge [
    source 40
    target 51
    relation "HAS_FUNCTION"
  ]
  edge [
    source 52
    target 53
    relation "HAS_FUNCTION"
  ]
  edge [
    source 52
    target 54
    relation "HAS_FUNCTION"
  ]
  edge [
    source 52
    target 55
    relation "HAS_FUNCTION"
  ]
  edge [
    source 52
    target 56
    relation "HAS_FUNCTION"
  ]
  edge [
    source 52
    target 57
    relation "HAS_FUNCTION"
  ]
  edge [
    source 52
    target 58
    relation "HAS_FUNCTION"
  ]
  edge [
    source 52
    target 59
    relation "HAS_FUNCTION"
  ]
  edge [
    source 60
    target 61
    relation "HAS_FUNCTION"
  ]
  edge [
    source 60
    target 62
    relation "HAS_FUNCTION"
  ]
  edge [
    source 60
    target 63
    relation "HAS_FUNCTION"
  ]
  edge [
    source 64
    target 65
    relation "HAS_FUNCTION"
  ]
  edge [
    source 64
    target 66
    relation "HAS_FUNCTION"
  ]
  edge [
    source 64
    target 67
    relation "HAS_FUNCTION"
  ]
  edge [
    source 64
    target 68
    relation "HAS_FUNCTION"
  ]
  edge [
    source 69
    target 70
    relation "HAS_FUNCTION"
  ]
  edge [
    source 69
    target 71
    relation "HAS_FUNCTION"
  ]
  edge [
    source 69
    target 72
    relation "HAS_FUNCTION"
  ]
]
