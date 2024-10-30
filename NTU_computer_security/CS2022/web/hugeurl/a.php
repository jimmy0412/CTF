<?php 

class Page
{
    public $url = "<?php echo '123';?>";
    private $title = "<?php echo '123';?>";
    private $preview = "<?php echo '123';?>" ;  
    // function __construct($url,$title,$preview)
    // {
    //     $this->url = $url;
    //     $this->title = $title;
    //     $this->preview = $preview;
    // }
}

class App
{
    protected $_callbacks = array(
        'path' => array(),
        'param' => array(),
        'method' => array(),
        'subdomain' => array(),
        'domain' => array(),
        'format' => array(),
        'custom' => array('')
    );
}

$n = new App();
$serialized_data = serialize($n);
file_put_contents('123',$serialized_data);

/*$m = new Page("http://localhost","<?php echo '123';?>","<?php echo '456';?>");*/
// $m = new Page();
// $serialized_data = serialize($m);
// file_put_contents('123',$serialized_data);
#system("curl -X POST 'http://localhost:10004/create' -d 'url=' ");
?>

<!--  curl -X POST "http://localhost:10004/create" -d "url= -->
