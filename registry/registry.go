package main

import (
	"flag"
	"github.com/gin-gonic/gin"
	"github.com/golang/glog"
	"io/ioutil"
	"net/http"
	"os"
)

var (
	version  = "dev"
	commit   = "none"
	date     = "unknown"
	hostname string
	registry = "https://ind.nl/Documents/Openbaar_register_Arbeid_Regulier_Kennismigranten.pdf"
)

func setupRouter() *gin.Engine {
	r := gin.Default()
	r.GET("/hc", healthCheck)
	r.GET("/version", getVersion)
	r.GET("/", statusOk) // kube default
	r.GET("/r", getRegistry)
	return r
}

func main() {
	var port string
	flag.StringVar(&port, "port", "5001", "server listening port")
	flag.Parse()

	hostname, _ = os.Hostname()
	router := setupRouter()
	router.Run(":" + port)
}

func getRegistry(c *gin.Context) {
	var req *http.Request
	var resp *http.Response
	var err error
	client := &http.Client{}

	glog.Info("--> GET " + registry)
	req, err = http.NewRequest("GET", registry, nil)
	resp, err = client.Do(req)
	if err != nil {
		c.JSON(http.StatusServiceUnavailable, gin.H{"error": err.Error()})
		return
	}
	defer resp.Body.Close()
	glog.Infof("<-- %d", resp.StatusCode)

	b, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		glog.Fatal(err)
	}
	err = ioutil.WriteFile("output.pdf", b, 0644)
	if err != nil {
		glog.Fatal(err)
	}

	c.JSON(resp.StatusCode, gin.H{"payload": resp.ContentLength})
}

func healthCheck(c *gin.Context) {
	c.String(http.StatusOK, "OK")
}

func getVersion(c *gin.Context) {
	body := gin.H{
		"version":  version,
		"commit":   commit,
		"date":     date,
		"hostname": hostname,
		"ginmode":  gin.Mode(),
		"lang":     "golang",
	}
	c.JSON(http.StatusOK, body)
}

func statusOk(c *gin.Context) {
	c.Status(http.StatusOK)
}
