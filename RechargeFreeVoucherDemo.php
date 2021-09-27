<?php
/**
 * Created by PhpStorm.
 * User: admin
 * Date: 2021/9/27
 * Time: 16:24
 * Class Demo
 * 微信支付商户免充值代金券接口升级验收
 */
class RechargeFreeVoucherDemo
{
    /**
     * @var int 请求方式
     * 1 使用curl
     * 2 使用插件 GuzzleHttp\Client
     */
    protected $requestType = 1;

    /**
     * @var string 32随机数
     */
    protected $nonceStr = '5K8264ILTKCH16CQ2502SDFSEMTMQEWE';

    /**
     * @var string 微信支付密钥
     */
    protected $signKey = ''; //todo

    /**
     * @var string 商户号
     */
    protected $mchId = ''; //todo

    /**
     * @var string 通过sign方法获取沙箱验签秘钥
     */
    protected $sandBoxKey = ''; //todo
    /**
     * @var bool 返回数据是否xml转化array
     */
    protected $openXmlArr = true;

    protected $appid = '';
    /**
     * 字段拼接
     */
    public static function getSignContent($data): string
    {
        $buff = '';
        foreach ($data as $k => $v) {
            $buff .= ('sign' != $k && '' != $v && !is_array($v)) ? $k . '=' . $v . '&' : '';
        }
        return trim($buff, '&');
    }

    /**
     *  作用：array转xml
     */
    function arrayToXml($arr)
    {
        $xml = "<xml>";
        foreach ($arr as $key => $val) {
            if (is_numeric($val)) {
                $xml .= "<" . $key . ">" . $val . "</" . $key . ">";
            } else
                $xml .= "<" . $key . "><![CDATA[" . $val . "]]></" . $key . ">";
        }
        $xml .= "</xml>";
        return $xml;
    }

    /**
     *  作用：将xml转为array
     */
    public function xmlToArray($xml)
    {
        //将XML转为array
        $array_data = json_decode(json_encode(simplexml_load_string($xml, 'SimpleXMLElement', LIBXML_NOCDATA)), true);
        return $array_data;
    }

    #签名
    public function getsignkey($data, $box = true)
    {
        $key = $this->sandBoxKey;
        #填写你的秘钥 ,后面几步用沙盒密钥
        if (!$box) $key = $this->signKey;

        ksort($data);
        // var_dump(self::getSignContent($data) . '&key=' . $key);die;
        $string = md5(self::getSignContent($data) . '&key=' . $key);
        return strtoupper($string);
    }

    #第一步 获取沙箱验签秘钥
    public function sign()
    {

        $data = [
            'mch_id'    => $this->mchId,
            'nonce_str' => $this->nonceStr,
        ];
        $data['sign'] = $this->getsignkey($data, false);
        $url = 'https://api.mch.weixin.qq.com/sandboxnew/pay/getsignkey';
        $result = $this->post($data, $url);
        if ($this->openXmlArr) if ($this->openXmlArr) $result = $this->xmlToArray($result);
        return $result;
    }

    #第二步 「1003-可选用例-公众号/APP/扫码正常支付」验收
    #1.统一下单
    public function pay()
    {
        //total_fee 必须为551
        $data = [
            'appid'            => 'wxd678efh567hg6787',
            'body'             => '测试商品',
            'mch_id'           => $this->mchId,
            'nonce_str'        => $this->nonceStr,
            'notify_url'       => 'http://www.weixin.qq.com/wxpay/pay.php',
            'out_trade_no'     => '201208241848',
            'spbill_create_ip' => '192.168.10.10',
            'total_fee'        => '552',
            'trade_type'       => 'JSAPI'
        ];
        $url = 'https://api.mch.weixin.qq.com/sandboxnew/pay/unifiedorder';
        $data['sign'] = $this->getsignkey($data);
        $result = $this->post($data, $url);
        if ($this->openXmlArr) $result = $this->xmlToArray($result);
        return $result;
    }

    #2.查询订单
    public function query()
    {
        $data = [
            'mch_id'       => $this->mchId,
            'nonce_str'    => $this->nonceStr,
            'out_trade_no' => '201208241848',
        ];
        $url = 'https://api.mch.weixin.qq.com/sandboxnew/pay/orderquery';
        $data['sign'] = $this->getsignkey($data);
        $result = $this->post($data, $url);
        if ($this->openXmlArr) $result = $this->xmlToArray($result);
        return $result;
    }

    #第三步 「1003-可选用例-公众号/APP/扫码支付退款」验收
    #1.申请退款
    public function refund()
    {
        //refund_fee 必须为552
        $data = [
            'appid'         => 'wxd678efh567hg6787',
            'mch_id'        => $this->mchId,
            'nonce_str'     => $this->nonceStr,
            'out_trade_no'  => '201208241848',
            'out_refund_no' => 'TM201208241848',
            'refund_fee'    => '552',
            'total_fee'     => '552',
        ];
        $data['sign'] = $this->getsignkey($data);
        $url = 'https://api.mch.weixin.qq.com/sandboxnew/pay/refund';
        $result = $this->post($data, $url);
        if ($this->openXmlArr) $result = $this->xmlToArray($result);
        return $result;
    }

    #2.查询退款
    public function refundquery()
    {
        $data = [
            'appid'        => 'wxd678efh567hg6787',
            'mch_id'       => $this->mchId,
            'nonce_str'    => $this->nonceStr,
            'out_trade_no' => '201208241848',
        ];
        $data['sign'] = $this->getsignkey($data);
        $url = 'https://api.mch.weixin.qq.com/sandboxnew/pay/refundquery';
        $result = $this->post($data, $url);
        if ($this->openXmlArr) $result = $this->xmlToArray($result);
        return $result;
    }

    #第四步 「1005-必选用例-交易对账单下载」 验收
    public function downloadbill()
    {
        $data = [
            'appid'        => 'wxd678efh567hg6787',
            'bill_date'    => '20120824',
            'bill_type'    => 'ALL',
            'mch_id'       => $this->mchId,
            'nonce_str'    => $this->nonceStr,
            'out_trade_no' => '201208241848',
        ];
        $data['sign'] = $this->getsignkey($data);
        $url = 'https://api.mch.weixin.qq.com/sandboxnew/pay/downloadbill';
        $result = $this->post($data, $url);
        return $result;
    }

    /**
     * @param $data
     * @param $url
     * post 请求
     */
    public function post($data, $url)
    {
        #两种请求方式
        if ($this->requestType === 1) {
            return $this->curlPost($data, $url);
        }
        if ($this->requestType === 2) {
            return $this->postXmlCurl($data, $url);
        }
        print_r('请求参数错误');
        exit;
    }

    /**
     *  作用：以post方式提交xml到对应的接口url
     */
    public function postXmlCurl($data, $url)
    {
        $xml = $this->arrayToXml($data);
        $httpClient = new Client();
        $response = $httpClient->request('POST', $url, ['body' => $xml]);
        $return = $response->getBody()->getContents();
        return $return;
    }

    /**
     * DateTime : 2021/8/24 19:03
     * curl 请求方式
     */
    public function curlPost($data, $url)
    {
        $xmlData = $this->arrayToXml($data);
        // var_dump($xmlData);die;
        $header[] = "Content-type: text/xml";        //定义content-type为xml,注意是数组
        $ch = curl_init($url);
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, $header);
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $xmlData);
        $response = curl_exec($ch);
        if (curl_errno($ch)) {
            print curl_error($ch);
        }
        curl_close($ch);
        return $response;
    }
}
$mch = new RechargeFreeVoucherDemo();
$pay = $mch->pay();
$query = $mch->query();
$refund =  $mch->refund();
$refundquery =  $mch->refundquery();
$downloadbill =  $mch->downloadbill();
//经测，1001，1002没有实现，1003用例会有无法验收的情况
var_dump($pay,$query);
