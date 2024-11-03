// models.go

package main

import (
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

type User struct {
	ID       uint   `gorm:"primaryKey"`
	Name     string `gorm:"size:100"`
	Email    string `gorm:"unique"`
	Age      int
	IsAdmin  bool `gorm:"default:false"`
	IsActive bool `gorm:"default:true"`
}

// Example Queries

func main() {
	// Initialize GORM with SQLite
	db, err := gorm.Open(sqlite.Open("example.db"), &gorm.Config{})
	if err != nil {
		panic("failed to connect database")
	}

	// Auto-migrate the schema
	db.AutoMigrate(&User{})

	// 1. Retrieve the first user
	var user User
	db.First(&user)

	// 2. Retrieve all users
	var users []User
	db.Find(&users)

	// 3. Filter users by name
	db.Where("name = ?", "John").Find(&users)

	// 4. Get a specific user by ID
	db.First(&user, 1) // Find user with primary key 1

	// 5. Exclude certain records
	db.Not("is_admin", true).Find(&users)

	// 6. Count the number of users
	var count int64
	db.Model(&User{}).Count(&count)

	// 7. Get users ordered by name
	db.Order("name").Find(&users)

	// 8. Perform an aggregate query (e.g., get average age)
	var avgAge float64
	db.Model(&User{}).Select("AVG(age)").Scan(&avgAge)

	// 9. Chain multiple filters
	db.Where("name LIKE ?", "J%").Where("is_active = ?", true).Find(&users)

	// 10. Using OR conditions
	db.Where("is_active = ? OR is_admin = ?", true, true).Find(&users)

	// 11. Update a user's email
	db.Model(&User{}).Where("id = ?", 1).Update("email", "newemail@example.com")

	// 12. Delete a user
	db.Delete(&User{}, 1) // Delete user with ID 1

	// 13. Group by and count users by role (assuming `role` field exists)
	var userCounts []struct {
		Role  string
		Count int64
	}
	db.Model(&User{}).Select("role, COUNT(*) as count").Group("role").Scan(&userCounts)

	// 14. Subquery to get users with specific conditions
	subquery := db.Model(&User{}).Select("id").Where("is_admin = ?", true)
	db.Where("id IN (?)", subquery).Find(&users)

	// 15. Complex join queries (assuming a Profile model is related to User)
	var usersWithProfiles []User
	db.Joins("JOIN profiles ON profiles.user_id = users.id").Where("profiles.age >= ?", 18).Find(&usersWithProfiles)

	// 16. Using HAVING clauses for filtering aggregates
	db.Model(&User{}).Select("role, COUNT(*) as user_count").Group("role").Having("user_count > ?", 5).Scan(&userCounts)

	// 17. Raw SQL for custom complex queries
	db.Raw("SELECT * FROM users WHERE age > ?", 18).Scan(&users)

	// 18. Transactions for complex operations
	db.Transaction(func(tx *gorm.DB) error {
		if err := tx.Create(&User{Name: "John", Email: "john@example.com"}).Error; err != nil {
			return err
		}
		return nil
	})

	// 19. Select specific columns
	var userData []struct {
		Name  string
		Email string
	}
	db.Model(&User{}).Select("name, email").Scan(&userData)

	// 20. Advanced filtering
	db.Where("name IN ?", []string{"John", "Jane"}).Find(&users)
	db.Where("email LIKE ?", "%example%").Find(&users)
}
