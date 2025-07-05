# SplashWarden
Convert SplashID export CSV file to Bitwwarden import format

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

### SplashId9toBW-csv.py
Format conversion tool to read SplashID 9 Pro exported CSV file and generate a Bitwarden CSV import file.
#### Clif Kranish 2025 (Based on SplashIDtoBW-csv.py by Glenn Seaton 2024)


**SplashID Pro 9** uses a new format when exporting a CSV file. Data is now exported with a value for field **name** and then three columns of data for each field: value, label, type. 
This program was developed with files exported from SpalshID Pro 9.3.20 

SplashID supports many pre-defined types and users can define their own. This program loads data from "Web Login" and several other common types based on their labels.  

The **Bitwarden** CSV file format has pre-defined fields plus a special field called **fields** that can contain name/value pairs for additonal fields. 
#### Catagory fields 
* Load Bitwarden **folders** from Splash ID "type" field 
* Ignore SplashID "category" field 
* Load Bitwarden **type** with value "login" which is the only type supported for CSV immport 
#### Standard fields 
* Load Bitwarden **login_username** with value from fields wtih labels: Username, User, Userid, 'User ID'
* Load Bitwarden **login_password** with value from fields with label: Password
* Load Bitwarden **login_uri** with value from fields with label: URL
#### Additonal fieds 
* Load Bitwarden **fields** with the following sub fields
  - "account" with values from fields with labels: Account , Number, Card, Card #, Policy #
  - "routing" wthe values form fields with labels: Routing
  - "pin" with the values from fields with labels: PIN
  - "Last_Update" with the value from field "update timestamp" converted to a readable format
  - Any other fields are loaded as "field2", "field3", etc. 

A file called "output.csv" is created that can be imported to Bitwarden from Tools > Import Data > File format > Bitwarden (csv) 

