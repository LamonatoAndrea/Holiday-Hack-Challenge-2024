<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Santa Vision</title>
    <!-- meta -->
    <meta name="description" content="">
    <meta name="author" content="">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <!-- styles -->
    <!-- CSS only -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-gH2yIJqKdNHPEq0n4Mqa/HGKIhSkIHeL5AyhkYV8i59U5AR6csBvApHHNl/vI1Bx" crossorigin="anonymous">
    <link rel="stylesheet" href="/static/css/styles.css">
    
  </head>
  <body>
    <!-- Navigation -->
<header class="p-3 mb-3 text-bg-dark">
  <div class="container">
    <div class="d-flex flex-wrap align-items-center justify-content-center justify-content-lg-start">
      <ul class="nav col-12 col-lg-auto me-lg-auto mb-2 justify-content-center mb-md-0">
        
      </ul>
      <div class="text-end">
        
      </div>
    </div>
  </div>
</header>
    <div id="outer" class="outer">
      <img id="sbnBackground" name="sbnBackground" src="./static/images/login.jpg" alt="">
      <img id="logo" name="logo" src="./static/images/logo.png" alt="">
      <div class="container">
      <!-- messages -->
        
        
        <div class="row">
          <div class="col-md-4"></div>
          <div class="col-md-4"></div>
          <div class="col-md-4"></div>
        </div>
        
        

        <!-- child template -->
        

<div class="row login-m">
	
    
	<div class="col-md-4">
		
        <div class="alert alert-danger alert-dismissible fade show alert-position" role="alert">
           Please log in to access this page.
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
		
	</div>
	
    
  <div class="col-md-4 form-position">
	<div class="line"></div>
    <main class="form-signin w-100 m-auto">
      <form role="form" method="post" action="">
        <input id="csrf_token" name="csrf_token" type="hidden" value="ImM2OTUxOWNlMDQyNmM4N2YxYjdhOTUyYTIwMTIxZmJiOGE0ZmZkZmYi.Z4A6pw.WEzZr_EnBzymjnKwK48ruYZMn20">
		
		
        <div class="mt-5 form-floating">
          <input class="form-control mb-2" id="username" name="username" placeholder="username" required type="text" value="">
          <label for="username">Username</label>
            
        </div>
        <div class="form-floating">
          <input class="form-control mb-2" id="password" name="password" placeholder="password" required type="password" value="">
          <label for="password">Password</label>
            
        </div>
        <button class="w-100 btn btn-lg btn-primary btn-signin" type="submit">Sign in</button>
      </form>
    </main>
  </div>
  <div class="col-md-4"></div>
</div>
<br>
<br>
<div class="footer" id="footer">
  <b>©2024 Santavision Elventech Co., Ltd. Snow Rights Reserved.<br>(<i>topic 'sitestatus'</i> available.)</b>
</div> <!-- mqtt: elfanon:elfanon -->

      </div>
    </div>
    <!-- scripts -->
    <script src="https://code.jquery.com/jquery-3.6.1.min.js" type="text/javascript"></script>
    <!-- JavaScript Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/js/bootstrap.bundle.min.js" integrity="sha384-A3rJD856KowSb7dwlZdYEkO39Gagi7vIsF0jrRAoQmDKKtQBHUuLZ9AsSv4jD4Xa" crossorigin="anonymous"></script>
    
  </body>
</html>